read str
iconv -f sjis -t UTF-8 $str > tmp.txt
textlint --fix tmp.txt
iconv -f UTF-8 -t sjis tmp.txt > $str
rm tmp.txt