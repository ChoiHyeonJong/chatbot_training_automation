#!/usr/bin/python
# -*- coding: UTF-8 -*-
# vi:ts=4:shiftwidth=4
# vim600:fdm=marker

# LG �����͸� ��<->���� ���� ���۽��� ��ȯ

import nltk
import sys, time, codecs
from optparse import OptionParser

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

"""
	CODER: HOON PAEK
"""
def convert_non_ascii_char(file_name):
	with open(file_name, mode='rb') as fid:
		before_text = fid.read()
	after_text = ''.join([i if ord(i) < 128 else ' ' for i in before_text])
	with open(file_name, mode='wb') as fid:
		fid.write(after_text)


def main():
	# Usage and Options {{{
	usage = "usage: %prog -d [options]"
	parser = OptionParser(usage)
	parser.add_option("-d", "--data", type="string", help="raw data file")
	(options, args) = parser.parse_args()
	# }}}

	if not options.data:
		parser.print_usage()
		sys.exit(1)

	# To cope with non-ascii character in data... (by HP)
	convert_non_ascii_char(options.data)

	infile = open(options.data, 'r')
	outfile_src = open(options.data+'.prev.txt', 'w') # ��
	outfile_tgt = open(options.data+'.next.txt', 'w') # ����
	prev_session = ''
	prev_user = 'BB'	# AA - ����, BB - ��
	src_cnt = tgt_cnt = 0
	for line in infile:
		line = line.replace('\n','')
		#print '---', line
		## data = line.split('\t')
		## if len(data) != 4:
        ## 		print >> sys.stderr, 'Error:', line
        ## break
		## session, user, _, sent = data
        data = line.split()
        if not data:
            continue
        session, user, sent = data[0], data[1], " ".join(data[3:])

		word = sent.split()
		if prev_session != session: # ������ �ٲ�
			# ���� ���� ������
			if src_cnt > tgt_cnt:
				print >> outfile_tgt
				tgt_cnt += 1
			elif src_cnt < tgt_cnt:
				print >> outfile_src
				src_cnt += 1
			if src_cnt != tgt_cnt:
				print >> sys.stderr, 'Error:', src_cnt, tgt_cnt
				#print "E2"
				#print line
				break
			# ���ο� ����
			if user == 'BB':
				#print "E1"
				#print line
				print >> outfile_src, ' '.join(nltk.word_tokenize(sent)),
			else:
				print >> outfile_src, '</s>'
				src_cnt += 1
				print >> outfile_tgt, ' '.join(nltk.word_tokenize(sent)),
		elif prev_user != user: # ��ȭ�ڰ� �ٲ�
			if user == 'AA': # ����
				# ���� �� ��ȭ newline
				print >> outfile_src
				src_cnt += 1
				# ���� ���� ��ȭ
				#print "err:", line 
				print >> outfile_tgt, ' '.join(nltk.word_tokenize(sent)),
			else: # ��
				# ���� ���� ��ȭ newline
				print >> outfile_tgt
				tgt_cnt += 1
				# ���� �� ��ȭ
				
				print >> outfile_src, ' '.join(nltk.word_tokenize(sent)),
		else: # ��ȭ�ڰ� �ȹٲ�
			if user == 'AA': # ����
				# ���� ���� ��ȭ
				print >> outfile_tgt, ' '.join(nltk.word_tokenize(sent)),
			else: # ��
				# ���� �� ��ȭ
				print >> outfile_src, ' '.join(nltk.word_tokenize(sent)),
		prev_session = session
		prev_user = user
	
	outfile_src.close()
	outfile_tgt.close()

if __name__ == "__main__":
    main()

