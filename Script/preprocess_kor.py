#! /usr/bin/python
# -*- coding: UTF-8 -*-
# vi:ts=4:shiftwidth=4
# vim600:fdm=marker

# LG �����͸� ��<->���� ���� ���۽��� ��ȯ

import sys, time, codecs
from optparse import OptionParser

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

	infile = open(options.data, 'r')
	outfile_src = open(options.data+'.src.txt', 'w') # ��
	outfile_tgt = open(options.data+'.tgt.txt', 'w') # ����
	prev_session = ''
	prev_user = 'BB'	# AA - ����, BB - ��
	src_cnt = tgt_cnt = 0
	for line in infile:
		line = line.replace('\n','')
		data = line.split('\t')
		if len(data) != 4:
			print >> sys.stderr, 'Error:', line
			break
		session, user, _, sent = data
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
				break
			# ���ο� ����
			if user == 'BB':
				print >> outfile_src, sent,
			else:
				print >> outfile_src, '</s>'
				src_cnt += 1
				print >> outfile_tgt, sent,
		elif prev_user != user: # ��ȭ�ڰ� �ٲ�
			if user == 'AA': # ����
				# ���� �� ��ȭ newline
				print >> outfile_src
				src_cnt += 1
				# ���� ���� ��ȭ
				print >> outfile_tgt, sent,
			else: # ��
				# ���� ���� ��ȭ newline
				print >> outfile_tgt
				tgt_cnt += 1
				# ���� �� ��ȭ
				print >> outfile_src, sent,
		else: # ��ȭ�ڰ� �ȹٲ�
			if user == 'AA': # ����
				# ���� ���� ��ȭ
				print >> outfile_tgt, sent,
			else: # ��
				# ���� �� ��ȭ
				print >> outfile_src, sent,
		prev_session = session
		prev_user = user
	
	outfile_src.close()
	outfile_tgt.close()

if __name__ == "__main__":
    main()

