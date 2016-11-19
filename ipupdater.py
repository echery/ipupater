#!/usr/bin/env python

'''
IPupdater: Update DNS records for dynamic IP addresses
Maintainer: Earl Chery <earl.chery@gmail.com>
''' 

import boto3
from requests import get
import argparse

# Set options to pass at startup.
parser = argparse.ArgumentParser( usage='%(prog)s [options]', description='Update DNS records automatically')
parser.add_argument('--cloud-provider', default='none')
parser.add_argument('--aws-secret-key')
parser.add_argument('--aws-access-key')
parser.add_argument('--aws-region', default='us-east-1')
parser.add_argument('--hostid')
parser.add_argument('--dns-record-name')

args = parser.parse_args()

aws_client = boto3.client(
	'route53',
	aws_access_key_id=args.aws_access_key,
	aws_secret_access_key=args.aws_secret_key,
	region_name=args.aws_region
)

def get_public_ip():
	ip = get('https://api.ipify.org').text
	return ip

def update_aws_dns_record():
	a_record = get_public_ip()
	
	try:
		response = aws_client.change_resource_record_sets(
		HostedZoneId=args.hostid,
		ChangeBatch={
			'Comment': 'Update Public IP',
			'Changes': [
				{
					'Action':'UPSERT',
					'ResourceRecordSet':{
						'Name': args.dns_record_name,
						'Type':'A',
						'TTL': 300,
						'ResourceRecords': [
							{
								'Value': a_record
							}
						]
					}
				}
			]
		}
		)
		print('Updated AWS Resource Record IP: ' + get_aws_dns_record())
	except:
		print("Unexpected error:", sys.exc_info()[0])

def get_aws_dns_record():
	dns_record = aws_client.list_resource_record_sets(
	    HostedZoneId=args.hostid,
	    StartRecordName=args.dns_record_name,
	    StartRecordType='A',
	    MaxItems='1'
	)
	
	if dns_record['ResourceRecordSets'][0]['Name'] != args.dns_record_name +'.':
		return 'null'
	else:
		return dns_record['ResourceRecordSets'][0]['ResourceRecords'][0]['Value']


print ('***************\n' + \
'** IPupdater **\n' + \
'***************')

print ('\nCurrent Public IP: ' + get_public_ip() + '\n')


if args.cloud_provider == 'aws':
	if args.aws_access_key is None or args.aws_secret_key is None or args.aws_region is None or args.hostid is None or args.dns_record_name is None:
		parser.error("Missing AWS option(s)")
	else:
		print ('Route53 DNS Record: ' + args.dns_record_name + '\n' + \
		'Current AWS Resource Record IP: ' + get_aws_dns_record())

		if get_aws_dns_record() == 'null': 
			update_aws_dns_record()
		elif get_aws_dns_record() != get_public_ip() :
			update_aws_dns_record()
		else:
			print('INFO: Record not modified')
