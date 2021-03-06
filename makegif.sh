#!/bin/sh
# Source https://youtu.be/V59q5DC9y6A
# convert a video into a gif animation

# Simple command "ffmpeg -ss 01 -t 14 -i input.mp4 -vf "fps=10,scale=1024:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" -loop 0 output.gif"
# script usage
usage()
{
# if argument passed to function echo it
[ -z "${1}" ] || echo "! ${1}"
# display help
echo "\
# convert a video into a gif animation

$(basename "$0") -s 00:00:00.000 -i infile.(mp4|mov|mkv|m4v) -t 00:00:00.000 -f [00] -w [0000] -o outfile.gif
-s 00:00:00.000 : start time
-i infile.(mp4|mov|mkv|m4v)
-t 00:00:00.000 : number of seconds after start time
-f [00]         : framerate
-w [0000]       : width
-o outfile.gif  :optional agument 
# if option not provided defaults infile-name-gif-date-time.gif"
exit 2
}

# error messages
NOTFILE_ERR='not a file'
INVALID_OPT_ERR='Invalid option:'
REQ_ARG_ERR='requires an argument'
WRONG_ARGS_ERR='wrong number of arguments passed to script'
NOT_MEDIA_FILE_ERR='is not a media file'

# if script is run arguments pass and check the options with getopts,
# else display script usage and exit
[ $# -gt 0 ] || usage "${WRONG_ARGS_ERR}"

# timecode - match 00:00:00
timecode='^[0-9]\{2\}:[0-9]\{2\}:[0-9]\{2\}([.]\{1\}[0-9]\{1,3\})?$'
fps_regex='^[0-9]\{1,2\}$'
width_regex='^[0-9]\{2,4\}$'

# getopts and check if input a file
while getopts ':s:i:t:f:w:o:h' opt
do
  case ${opt} in
     s) start="${OPTARG}"
         expr "${start}" : "${timecode}" 1>/dev/null;;
     i) infile="${OPTARG}"
	[ -f "${infile}" ] || usage "${infile} ${NOTFILE_ERR}";;
     t) end="${OPTARG}"
        expr "${end}" : "${timecode}" 1>/dev/null;;
     f) framerate="${OPTARG}"
        expr "${framerate}" : "${fps_regex}" 1>/dev/null;;
     w) width="${OPTARG}"
        expr "${width}" : "${width_regex}" 1>/dev/null;;
     h) usage;;
     o) outfile="${OPTARG}";;
     \?) usage "${INVALID_OPT_ERR} ${OPTARG}" 1>&2;;
     :) usage "${INVALID_OPT_ERR} ${OPTARG} ${REQ_ARG_ERR}" 1>&2;;
  esac
done
shift $((OPTIND-1))

# infile name
infile_nopath="${infile##*/}"
infile_name="${infile_nopath%.*}"

# file command check input file mime type
filetype="$(file --mime-type -b "${infile}")"

# video mimetypes
mov_mime='video/quicktime'
mkv_mime='video/x-matroska'
mp4_mime='video/mp4'
m4v_mime='video/x-m4v'

# defaults for variables if not defined
start_default='00:00:00'
end_default=$(ffprobe -v error -sexagesimal -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$infile" | cut -d\. -f1)
framerate_default='10'
width_default='1024'
outfile_default="${infile_name}-gif-$(date +"%Y-%m-%d-%H-%M-%S").gif"

# create gif function
create_gif () {
    ffmpeg \
    -hide_banner \
    -stats -v panic \
    -ss "${start:=${start_default}}" \
    -i "${infile}" \
    -t "${end:=${end_default}}" \
    -filter_complex "[0:v] fps=${framerate:=${framerate_default}},scale=${width:=${width_default}}:-1:flags=lanczos,split [a][b];[a] palettegen [p];[b][p] paletteuse" \
    "${outfile:=${outfile_default}}"
}

# check the files mime type
case "${filetype}" in
    ${mov_mime}|${mkv_mime}|${mp4_mime}|${m4v_mime}) create_gif "${infile}";;
    *) usage "${infile} ${NOT_MEDIA_FILE_ERR}";;
esac

