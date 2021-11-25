from moviepy.editor import ImageSequenceClip
import os
import subprocess


class GifMaker(object):

    """
    Parameters:
        - auto_compress:
            whether compress gif result when size excceed threshold
        
        - compress_threshold: 
            size of gif compress threshold, in KB
    """
    def __init__(self, auto_compress=True, compress_threshold=None) -> None:
        super().__init__()
        self.auto_compress = auto_compress
        self.compress_threshold = compress_threshold


    def make_gif(self, img_paths:list, gif_name:str, fps:int, colors:int):
        if gif_name is None or not gif_name.endswith(".gif"):
            raise ValueError("Given destination path invalid.")
        self.gif_name = gif_name

        clip = ImageSequenceClip(img_paths, fps)
        clip.write_gif(gif_name, program='imageio', opt='nq', fps=fps, fuzz=0, colors=colors)

        if self.auto_compress and self.compress_threshold > 0:
            self.check_gif(gif_name)


    def check_gif(self, gif_path:str):
        gif_size = os.stat(gif_path).st_size
        print("gif size: %d" % gif_size)

        if gif_size > self.compress_threshold * 1000:   # 超过阈值做gif压缩
            self.compress_gif(gif_path)


    """
    Adjust parameter [optimize_level] to get smaller size,
    currently max value is 3.
    """
    def compress_gif(self, gif_path=None, optimize_level=3, options=None):
        sources = [gif_path]
        if any([not source.endswith(".gif") for source in sources]):
            raise ValueError("Given source path is not a gif image.")
        destination = 'Z_' + sources[0]

        if options is None:
            options = []
        options.append("--unoptimize")
        options.append("--optimize=" + str(optimize_level))

        subprocess.call(["gifsicle", *options, *sources, "--output", destination])


if __name__ == '__main__':
    gif_maker = GifMaker(auto_compress=True, compress_threshold=1000)
    img_files = ['gif_test/figures/'+str(i)+'.jpg' for i in range(0,15)]
    gif_maker.make_gif(img_files, 'test1.gif', fps=15, colors=256)
    # gif_maker.compress_gif('special_effects_maker_sr_f17a26b02a9011ecb038b4055d45ef6d_test.gif')