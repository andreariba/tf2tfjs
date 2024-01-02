#!/bin/bash
set -e

while getopts u:t:c:f: flag
do
    case "${flag}" in
        u) upload=${OPTARG};;
        t) tmp=${OPTARG};;
        c) convert=${OPTARG};;
        f) filename=${OPTARG};;
    esac
done
echo "Filename: $filename";
echo "Upload folder: $upload";
echo "Temp folder: $tmp";
echo "Converted folder: $convert";

unzip "./$upload/$filename.zip" "-d" "$tmp/$filename"

tensorflowjs_converter \
    --input_format tf_saved_model \
    --output_format=tfjs_graph_model \
    --output_node_names='policy,value' \
    --saved_model_tags=serve \
    "./$tmp/$filename" \
    "./$convert/$filename"

#zip -rm "$convert/$filename.zip "$convert/$filename"
tar czf "./$convert/$filename.tar.gz" "./$convert/$filename"

# cleanup
rm -rf "./$tmp/$filename" "./$convert/$filename" "./$upload/$filename.zip"

