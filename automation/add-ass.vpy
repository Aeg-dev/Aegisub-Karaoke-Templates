import vapoursynth as vs


v_fname = "gary-1080p-4s.mp4"
ass_fname = "fx-applied.ass"

core = vs.get_core(threads=8)
core.max_cache_size = 2000

src = core.lsmas.LWLibavSource(v_fname, threads=1)
src = core.vsfm.TextSubMod(src, ass_fname)
src.set_output()
