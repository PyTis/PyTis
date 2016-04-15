
import getpass
import datetime
import os
import collections
import requests
import csv
import logging
from collections import defaultdict
import subprocess


def get_ec2_info(apikey, keys, required=None, verifySSL=True):
    """
    apikey = api key to use to connect to cloudcheckr
    keys = list of strings with field names to return
    required (optional) = string of field name that cannot be None
    verifySSL (optional) = set to false to ignore invalid SSL certificates

    Returns list of info for instances
    """
    url = 'https://api2.cloudcheckr.com/api/inventory.json/get_resources_ec2_details'
    payload = {'access_key': apikey, 'use_account': 'BAH (Everything)'}

    hasnext = True
    instance_info = list()

    print "Retrieving information... this may take a few minutes"

    while hasnext:
        print "working..."
        r = None
        r = requests.get(url, params=payload, verify=verifySSL)
        print r.status_code
        if r.status_code == 200:
            try:
                results = r.json()
                for instance in results['Ec2Instances']:
                    if required:
                        if instance[required] == None:
                            continue
                    tmp = dict()
                    for key in keys:
                        tmp[key] = instance[key]
                    instance_info.append(tmp)
            except KeyError, e:
                print "Error: {}".format(e)
                logging.error(r.text)
                return None

        else:
            print "There was an error"
            print r.text
        hasnext = results['HasNext']
        if hasnext == True:
            payload['next_token'] = results['NextToken']

    return instance_info


# This function takes a CSV file as an input and generates a target list from the PublicIpAddress column
# The targets.txt file goes into the "dir" location
def create_targets(file, dir):
    # each value in each column is appended to a list
    columns = defaultdict(list)

    with open(file) as f:
        # read rows into a dictionary format
        reader = csv.DictReader(f)

        # read a row as {column1: value1, column2: value2,...}
        for row in reader:

            # go over each column name and value
            for (k, v) in row.items():
                # append the value into the appropriate list based on column name k
                columns[k].append(v)

    # Create a comma-separated string of IP from the list
    targetslist = "\n".join(columns['PublicIpAddress'])

    # Write all IPs to a targets file
    f = open(dir + '/targets.txt', 'w')
    f.write(targetslist + '\n')
    f.close()


# Function to run NMAP on a list of IPs. The scan results will be in "dir" location with all output formats
def run_nmap(dir):
    targets = dir + '/targets.txt'
    subprocess.call(["nmap", "-vv", "-A", "-sV", "-Pn", "-T4", "-iL", targets, "-oA", dir + "/nmap-scan"])

    # Create an HTML report
    subprocess.call(["xsltproc", dir + "/nmap-scan.xml", "-o", dir + "/nmap-scan.html"])


# Function to convert NMAP output to CSV
def run_nmap_parser(dir):
    scanfile = dir + '/nmap-scan.xml'
    subprocess.call(["python", "nmap-parser-xml-to-csv/nmap-parser-xml-to-csv.py", scanfile, "-s", ",", "-o",
			dir + "/nmap-scan.csv"])


# Function to run PeepingTom with the results from NMAP scan. The scan results will be in "dir" location
def run_peepingtom(dir):
    scanfile = dir + '/nmap-scan.xml'
    subprocess.call(["python", "peepingtom/peepingtom.py", "-x", scanfile, "-o", dir + "/peepcaptures/"])


# Function to sort the NMAP findings by IP and port numbers
def sort_ip_ports(file, dir):
    d_ip = collections.defaultdict(set)

    with open("file", "r") as f_input:
        csv_input = csv.reader(f_input, skipinitialspace=True)
        headers = next(csv_input)

        for row in csv_input:
            d_ip[row[0]].add(row[1])
            # d_ip[row[0]].append(row[1])

    with open("dir/instances_with_open_ports.csv", "wb") as f_output:
        csv_output = csv.writer(f_output)
        csv_output.writerow(headers)
        print "%-20s %s" % (headers[0], headers[1])

        # Sort by IP address
        ip_sorted = d_ip.keys()
        ip_sorted.sort(key=lambda x: socket.inet_aton(x))

        for ip in ip_sorted:
            l_ports = list(d_ip[ip])
            l_ports.sort(key=lambda x: int(x))
            csv_output.writerow([ip, ", ".join(l_ports)])
            print "%-20s %s" % (ip, ", ".join(l_ports))


# Function to sort and correlate IPs/Open ports. It requires CSV file from nmap-parser tool
def sort_ip_ports(infile, outdir):
    outfile = outdir + '/ips_with_open_ports.csv'

    d_ip = collections.defaultdict(set)

    with open(outdir + '/' + infile, "r") as f_input:
        csv_input = csv.reader(f_input, skipinitialspace=True)
        headers = next(csv_input)

        for row in csv_input:
            d_ip[row[0]].add(row[1])
            # d_ip[row[0]].append(row[1])

    with open(outfile, "wb") as f_output:
        csv_output = csv.writer(f_output)
        csv_output.writerow(headers)
        print "%-20s %s" % (headers[0], headers[1])

        # Sort by IP address
        ip_sorted = d_ip.keys()
        ip_sorted.sort(key=lambda x: socket.inet_aton(x))

        for ip in ip_sorted:
            l_ports = list(d_ip[ip])
            l_ports.sort(key=lambda x: int(x))
            csv_output.writerow([ip, ", ".join(l_ports)])
            print "%-20s %s" % (ip, ", ".join(l_ports))


# Append two CSV files
def append_to_report(file1, file2, outdir):
    df_old = pd.read_csv(outdir + '/' + file1)
    df_new = pd.read_csv(outdir + '/' + file2)
    df_merged = df_old.merge(df_new, left_on="PublicIpAddress", right_on="PublicIpAddress", how="outer")
    df_merged.to_csv(outdir + '/' + file1, index=False)


def main():
    # Create output folder with the date. This is where all files will be stored
    outputdir = os.path.join(os.getcwd(), datetime.datetime.now().strftime('%Y-%m-%d'))
    os.makedirs(outputdir)

    logging.basicConfig(filename=outputdir + "/errors.log")

    # Create the output CSV file inside the folder
    outputfile = outputdir + '/Cloudcheckr-' + datetime.datetime.now().strftime("%Y%m%d-%H%M") + '.csv'

    if not os.path.exists(os.path.dirname(outputfile)):
        os.makedirs(os.path.dirname(outputfile))

    apikey = getpass.getpass('Enter admin API key: ')

    # fields to get
    fields = ['InstanceId', 'InstanceName', 'AccountName', 'Platform', 'PublicDnsName', 'PublicIpAddress', 'Status', 'Cost',]

    info_list = get_ec2_info(apikey, fields, required='PublicIpAddress', verifySSL=False)

    if info_list:
        try:
            with open(outputfile, 'wb') as wh:
                writer = csv.DictWriter(wh, fieldnames=fields)
                writer.writeheader()
                for item in info_list:
                    writer.writerow(item)
        except Exception, e:
            print info_list
    else:
        print 'Something broke'

    # Call function to generate the NMAP targets list
    create_targets(outputfile, outputdir)

    # Run NMAP and create XML scan report in the output folder
    run_nmap(outputdir)

    # Run NMAP-parser
    run_nmap_parser(outputdir)

    # Run PeepingTom
    run_peepingtom(outputdir)

    # Sort the IPs and open ports
    sort_ip_ports('nmap-scan.csv', outputdir)

    # Append open ports to the main spreadsheet to the main
    append_to_report(outputfile, 'ips_with_open_ports.csv', outputdir)


if __name__ == '__main__':
    main()


