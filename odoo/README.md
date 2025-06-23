# Odoo Personal Finance Management Modules

Custom Odoo modules for the Mindbots Personal Finance Management system.

## Overview

This directory contains custom Odoo 16.0 modules that provide:
- Core financial data models
- Banking integration
- Financial reporting
- AI agent integration
- Budget management
- Transaction tracking

## Module Structure

### pfm_core
Core module providing base functionality:
- Account and transaction models
- User preferences
- Base API endpoints

### pfm_banking
Banking integration features:
- Bank account management
- Transaction synchronization
- Statement import

### pfm_reporting
Financial reporting and analytics:
- Custom financial reports
- Budget vs actual analysis
- Cash flow reports

### pfm_ai_integration
Integration with AI agents:
- Transaction classification hooks
- Receipt matching integration
- Financial insights display

## Installation

1. Copy modules to Odoo addons path:
```bash
cp -r addons/* /mnt/extra-addons/
```

2. Update Odoo configuration:
```bash
cp config/odoo.conf /etc/odoo/
# Edit configuration as needed
```

3. Restart Odoo and update module list:
```bash
systemctl restart odoo
# In Odoo: Apps > Update Apps List
```

4. Install modules:
- Install `pfm_core` first
- Then install other modules as needed

## Development

### Prerequisites
- Odoo 16.0 Community Edition
- PostgreSQL 14+
- Python 3.10+

### Local Development
```bash
# Start Odoo in development mode
odoo -c config/odoo.conf --dev=all
```

### Creating New Modules
```bash
odoo scaffold module_name addons/
```

## Configuration

Key settings in `odoo.conf`:
- `db_name`: Database name (default: pfm)
- `addons_path`: Include custom addons directory
- `workers`: Number of worker processes
- `dev_mode`: Enable for development

## API Access

The modules provide REST API endpoints:
- `/api/pfm/accounts` - Account management
- `/api/pfm/transactions` - Transaction data
- `/api/pfm/reports` - Financial reports

## License

Proprietary - Mindbots Inc. All rights reserved.