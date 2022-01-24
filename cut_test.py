import subprocess as sp
import math


def trans_ts(filename, outfile):
    cmd = f"ffmpeg -y -i {filename} -vcodec copy -acodec copy -vbsf h264_mp4toannexb {outfile}"
    p = sp.Popen(cmd, shell=True)
    p.wait()
    return


def cut_video(filename, outfile, start, length=90):
    cmd = "ffmpeg -y -i %s -ss %d -t %d -c copy %s" % (filename, start, length, outfile)
    p = sp.Popen(cmd, shell=True)
    p.wait()
    return


def get_video_duration(filename):
    cmd = "ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 -i %s" % filename
    p = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE)
    p.wait()
    strout, strerr = p.communicate()  # 去掉最后的回车
    ret = strout.decode("utf-8").split("/n")[0]
    return ret


def concat_video(filename_list):
    cmd = f"ffmpeg -y -f concat -safe 0 -i {filename_list} -c copy concat.mp4"
    p = sp.Popen(cmd, shell=True)
    p.wait()
    return


def main():
    filename = 'static/video/demo1.mp4'
    length = 16
    length_drop = 12
    start = 1000
    start = 0

    trans_ts(filename, f'out/ts/demo.ts')
    duration = math.floor(float(get_video_duration(filename)))
    part = math.ceil(duration / length)
    # part = 30
    files = []
    for i in range(start, start + part*length, length):
        cut_video(f'out/ts/demo.ts', f'out/pieces/test_{i//length}.ts', i, length-length_drop)
        files.append(f"file 'F:/Projects/toolkit/video_cut/out/pieces/test_{i//length}.ts'")
    #
    filename_new = 'F:/Projects/toolkit/video_cut/file_pieces.txt'
    with open(filename_new, 'w', encoding='utf-8') as f_piece:
        f_piece.write('\n'.join(files))

    concat_video(filename_new)


if __name__ == '__main__':
    main()
