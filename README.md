## ipupdater

Public IP update tool for dynamic DNS connections


## Description

This tool automatically discovers the current public IP address and provides the option to update AWS Route53 DNS records with the discovered address.

## Usage

##### Get the current public IP address
```
docker run --rm echery/ipupdater
```

##### Updating AWS Route53

**Note:** This requires the host ID of the domain name to apply DNS records updates to. This can be found by clicking on the root domain in Route53 where the Host ID will be displayed.

```
docker run --rm echery/ipupdater \
--cloud-provider aws \
--aws-access-key <AWS_ACCESS_KEY> \
--aws-secret-key <AWS_SECRET_ACCESS_KEY \
--aws-region <AWS_REGION> \
--hostid <AWS_ROUTE53_HOSTID> \
--dns-record-name <DESIRED_DNS_RECORD>
```