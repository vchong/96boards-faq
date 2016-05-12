This repo is a quick hack to automatically prepare the FAQ nursery (on the
96boards github wiki) and convert it to a form that can be copy 'n pasted
onto the 96boards forum. It splits out the first level heading from the
FAQ nursery, converts the resulting markdown fragments into HTML and then
sanitizes the output so it contains only tags suitable for uploading
to the forum.

The idea behind the tool is to commit the .wp files every time the forum
is updated. This results in a workflow to update the forum as follows:

  make
  git diff
  <manually update the forum from the .wp files>
  git commit -a "Contents of the forum as of $(date)"

