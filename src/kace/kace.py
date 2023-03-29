import redis
from pprint import pprint
import json
import requests
import hvac
import os
import sys
import datetime
import pynetbox

def prettyllog(function, action, item, organization, statuscode, text):
  d_date = datetime.datetime.now()
  reg_format_date = d_date.strftime("%Y-%m-%d %I:%M:%S %p")
  print("%-20s: %-12s %20s %-50s %-20s %-4s %-50s " %( reg_format_date, function,action,item,organization,statuscode, text))

class Hvac:
  def __init__(self):
    self.url = self._get_url()
    self.token = self._get_token()
    self.client = hvac.Client(url=self.url, token=self.token)

  @staticmethod
  def _get_url():
    return os.getenv(key="VAULT_URL")

  @staticmethod
  def _get_token():
    return os.getenv(key="VAULT_TOKEN")

  # Method to create a new KV pair
  def create_kv_engine(self, engine_name):
    self.client.sys.enable_secrets_engine(
      backend_type="kv",
      path=engine_name,
      options={"version": "2"}
    )

  # Method to create a password 
  def create_password(self, engine_name, username, password):
    self.client.secrets.kv.v2.create_or_update_secret(
      mount_point=engine_name,
      path=username,
      secret={"username": username, "password": password}
    )

  # Method to read an existing password 
  def read_password(self, engine_name, username):
    return self.client.secrets.kv.v2.read_secret_version(
      mount_point=engine_name,
      path=username
    )
  # Method to read an existing token
  def read_secret(self, engine_name, secret):
    return self.client.secrets.kv.v2.read_secret_version(
      mount_point=engine_name,
      path=secret
    )
def netbox_cleanup(url, token):
  nb = pynetbox.api(
    url=url,
    token=token
  )


  ipranges = nb.ipam.ip_ranges.all()
  ipaddresses = nb.ipam.ip_addresses.all()
  sites = nb.dcim.sites.all()
  regions = nb.dcim.regions.all()
  locations = nb.dcim.locations.all()
  tenants = nb.tenancy.tenants.all()
  tenantgroups = nb.tenancy.tenant_groups.all()
  contacts = nb.dcim.contacts.all()
  contactgroups = nb.dcim.contact_groups.all()
  contactroles = nb.dcim.contact_roles.all()
  sitegroups = nb.dcim.site_groups.all()
  devices = nb.dcim.devices.all()
  devicetypes = nb.dcim.device_types.all()
  deviceroles = nb.dcim.device_roles.all()



  nb.dcim.devices.delete(devices)
  nb.dcim.sites.delete(sites)
  nb.dcim.site_groups.delete(sitegroups)
  nb.dcim.regions.delete(regions)
  nb.ipam.ip_addresses.delete(ipaddresses)
  nb.ipam.ip_ranges.delete(ipranges)
  nb.tenancy.tenants.delete(tenants)
  nb.tenancy.tenant_groups.delete(tenantgroups)




########################################################################################################################
# Main:  start
########################################################################################################################

def kace():
    print("Knowit Automated CMDB enabler")
    nburl = os.getenv("NETBOXURL")
    nbtoken = os.getenv("NETBOXTOKEN")
    netbox_cleanup(nburl, nbtoken)



### The end
