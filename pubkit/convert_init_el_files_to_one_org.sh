#!/usr/bin/env bash

sed -n "s/^(require \'\(init-[^ )]*\).*/\1.el/p" ../init.el|while read file; do echo ""\*\* ""$file;echo "#+BEGIN_SRC emacs-lisp"; cat $file; echo "#+END_SRC"; done >all-init.org