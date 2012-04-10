#!/usr/bin/python
# -*- encoding: utf-8 -*-

##############################################################################
#
#    Realizzata da Francesco OpenCode Apruzzese
#    Compatible with OpenERP release 6.0.X GTK Client
#    Copyright (C) 2012 Francesco Apruzzese. All Rights Reserved. Under GPL 3 Licence
#    Email: cescoap@gmail.com
#    Web site: http://www.e-ware.org
#
##############################################################################

import popen2
import os
import sys


def main(openerp_gtk_client_path):
	# ----- Escape if config file with client list doesn't exist
	print 'Reading customer list file...'
	customer_list_path = '%s/config/customer.list' % (os.path.dirname(sys.argv[0]))
	if not os.path.exists(customer_list_path):
		print 'Create "customer.list" file in "config" folder!'
		return False
	# ----- Open the config list file and extracts customers list
	config_file = open(customer_list_path,'r')
	customer_list_file = config_file.readlines()
	print 'Parding customer list file...'
	# ----- Create the bash windows parametrs, show it and keep the selection
	customer_list = ' '.join(cliente.split('\t')[0].replace('\n', '') for cliente in customer_list_file)
	print 'Creating data window...'
	bash_string = 'zenity --list --text="Select a line:" --column="Customers" %s' % (customer_list)
	result = popen2.popen3(bash_string)
	selected_customer = result[0].readlines()[0].replace('\n', '')
	# ----- Extracts the customer ip
	customer_ip = ''
	customer_port = '8070'
	for customers in customer_list_file:
		if customers.split('\t')[0] == selected_customer:
			customer_ip = customers.split('\t')[1]
			if len(customers.split('\t')) > 2:
				customer_port = customers.split('\t')[2]
	print 'Setting remote IP to', customer_ip.replace('\n', ''), '...'
	print 'Setting remote PORT to', customer_port, '...'
	return customer_ip.replace('\n', ''), customer_port


if __name__ == '__main__':
	print '\n==========================================='
	print 'Welcome to OpenERP Remote Rapid Connection'
	print ''
	print 'Developed by "Francesco OpenCode Apruzzese"'
	print 'cescoap@gmail.com - http://e-ware.org'
	print '===========================================\n'
	if len(sys.argv) >= 2:
		openerp_gtk_client_path = sys.argv[1]
		customer_ip, customer_port = main(openerp_gtk_client_path)
		if customer_ip:
			bash_string = '%s -l debug_rpc_answer -p %s -s %s' % (openerp_gtk_client_path, customer_port, customer_ip)
			print 'Executing', bash_string
			os.system(bash_string)
	else:
		print 'Set your OpenERP GTK Client path!'
