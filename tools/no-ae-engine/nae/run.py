# Полный прогон: проект → events.json → рендер (параллельно кусками) → микс → мастер CRF 14 + light CRF 18 → QA → контакт-лист.
#   python -m nae.run project.py --out out/ [--voice voice.wav] [--sfx-root .../assets/sfx] [--jobs 4]
#   python -m nae.run project.py --out out/ --frames 1.0,3.5,7.2     # только стиль-фреймы PNG (этап 4)
#   python -m nae.run project.py --out out/ --draft                  # быстрый черновик 540×960 без QA
# Проект — .py с функцией build() -> Comp (необязательно: VOICE = путь к голосу, REF_TEMPO = True).
import argparse, importlib.util, json, os, subprocess, sys, time, shutil
from multiprocessing import Pool
import numpy as np, cv2

def load_project(path):
    spec = importlib.util.spec_from_file_location('project', path)
    m = importlib.util.module_from_spec(spec); sys.path.insert(0, os.path.dirname(os.path.abspath(path)))
    spec.loader.exec_module(m); return m

_COMP = None
def _init(path):
    global _COMP
    _COMP = load_project(path).build()

def _chunk(args):
    a, b, seg, scale = args
    c = _COMP
    w, h = (c.w, c.h) if scale == 1 else (c.w // scale, c.h // scale)
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{w}x{h}', '-r', str(c.fps),
                          '-i', '-', '-c:v', 'libx264', '-preset', 'ultrafast', '-qp', '0', '-pix_fmt', 'yuv444p', seg],
                         stdin=subprocess.PIPE)
    for n in range(a, b):
        f = c.frame8(n)
        if scale != 1: f = cv2.resize(f, (w, h), interpolation=cv2.INTER_AREA)
        p.stdin.write(f.tobytes())
    p.stdin.close(); p.wait()
    return b - a

ENC = ['-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709',
       '-movflags', '+faststart']
VF709 = 'scale=out_color_matrix=bt709:out_range=tv:flags=lanczos'

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('project'); ap.add_argument('--out', required=True)
    ap.add_argument('--voice'); ap.add_argument('--sfx-root', default=os.environ.get('NAE_SFX'))
    ap.add_argument('--jobs', type=int, default=os.cpu_count()); ap.add_argument('--frames')
    ap.add_argument('--draft', action='store_true'); ap.add_argument('--name', default=None)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    proj = load_project(a.project); comp = proj.build()
    name = a.name or getattr(proj, 'NAME', os.path.splitext(os.path.basename(a.project))[0])
    voice = a.voice or getattr(proj, 'VOICE', None)

    if a.frames:   # стиль-фреймы / кадры для просмотра
        for t in map(float, a.frames.split(',')):
            cv2.imwrite(f'{a.out}/frame_{t:05.2f}.png', cv2.cvtColor(comp.frame8(int(round(t * comp.fps))), cv2.COLOR_RGB2BGR))
        print('кадры готовы'); return

    t0 = time.time()
    events = comp.events()
    json.dump(events, open(f'{a.out}/events.json', 'w'), ensure_ascii=False, indent=0)
    iss = comp.issues()
    if iss: print('ВНИМАНИЕ:', *iss, sep='\n  ')

    N = comp.nframes(); jobs = max(1, a.jobs); step = max(15, -(-N // (jobs * 3)))
    tmp = f'{a.out}/_seg'; os.makedirs(tmp, exist_ok=True)
    tasks = [(s, min(N, s + step), f'{tmp}/{i:04d}.mkv', 2 if a.draft else 1) for i, s in enumerate(range(0, N, step))]
    with Pool(jobs, initializer=_init, initargs=(os.path.abspath(a.project),)) as pool:
        done = 0
        for k in pool.imap_unordered(_chunk, tasks):
            done += k; print(f'\rрендер {done}/{N}', end='', flush=True)
    print(f'  ({time.time() - t0:.0f} с)')
    with open(f'{tmp}/list.txt', 'w') as f:
        for *_, seg, _s in tasks: f.write(f"file '{os.path.abspath(seg)}'\n")

    from .mix import mix
    mix_wav = f'{a.out}/{name}_mix.wav'
    info = mix(events, mix_wav, comp.dur, voice=voice, sfx_root=a.sfx_root, audit=f'{a.out}/sfx_audit.tsv')
    print('SFX:', info['n'], 'событий', ('| ЗАГЛУШКИ вместо библиотеки: ' + ', '.join(info['synth'])) if info['synth'] else '')

    src = ['-f', 'concat', '-safe', '0', '-i', f'{tmp}/list.txt', '-i', mix_wav]
    if a.draft:
        out = f'{a.out}/{name}_draft.mp4'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', *src, '-vf', VF709, *ENC, '-crf', '23', '-preset', 'veryfast',
                        '-c:a', 'aac', '-b:a', '192k', '-shortest', out], check=True)
        shutil.rmtree(tmp); print('черновик:', out); return
    master, light = f'{a.out}/{name}_master.mp4', f'{a.out}/{name}_1080.mp4'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', *src, '-vf', VF709, *ENC, '-crf', '14', '-preset', 'slow',
                    '-c:a', 'aac', '-b:a', '320k', '-shortest', master], check=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', *src, '-vf', VF709, *ENC, '-crf', '18', '-preset', 'slow',
                    '-c:a', 'aac', '-b:a', '256k', '-shortest', light], check=True)
    shutil.rmtree(tmp)
    # контакт-лист: 12 кадров
    n = 12; ts = [comp.dur * (i + 0.5) / n for i in range(n)]
    tiles = [cv2.resize(cv2.cvtColor(comp.frame8(int(t * comp.fps)), cv2.COLOR_RGB2BGR), (270, 480), interpolation=cv2.INTER_AREA) for t in ts]
    for im, t in zip(tiles, ts): cv2.putText(im, f'{t:.1f}s', (8, 470), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 200, 255), 2)
    cv2.imwrite(f'{a.out}/{name}_sheet.jpg', np.vstack([np.hstack(tiles[i:i + 6]) for i in (0, 6)]), [cv2.IMWRITE_JPEG_QUALITY, 88])

    from . import qa
    ok, rep = qa.run(comp, a.out, master, light, mix_wav, events, voice=bool(voice), ref_tempo=getattr(proj, 'REF_TEMPO', False))
    print(rep); print('итого', f'{time.time() - t0:.0f} с')
    sys.exit(0 if ok else 2)

if __name__ == '__main__':
    main()
