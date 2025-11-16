ALLOWED_CHILD = {
    'super_master_distributor': ['master_distributor', 'distributor', 'retailer'],
    'master_distributor': ['distributor', 'retailer'],
    'distributor': ['retailer'],
    'retailer': [],
}
