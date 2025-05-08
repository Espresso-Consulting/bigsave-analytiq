# BigQuery Tables Imported from Espresso Test Data.xlsx

The following tables were created in the `bigsave.demo` dataset by uploading each sheet from the Excel file `Espresso Test Data.xlsx`:

| Sheet Name           | Table Name                  | Rows     | Columns |
|----------------------|----------------------------|----------|---------|
| Stock                | stock                      | 88,278   | 35      |
| Stock Master         | stock_master               | 105,546  | 36      |
| Purchases            | purchases                  | 52,967   | 22      |
| Sales other info     | sales_other_info           | 1,866    | 3       |
| Stock Onhands        | stock_onhands              | 11,014   | 8       |
| Suppliers            | suppliers                  | 1,416    | 6       |
| Sales                | sales                      | 1,048,575| 21      |
| Stock Taxan          | stock_taxan                | 1,048,575| 7       |

- All columns were uploaded as string type.
- Table names are sanitized (spaces replaced with underscores, lowercased).
- Each table was overwritten if it already existed.

You can use this file for future reference and to inform further conversations about the available tables.

## Table Structures

### stock
Columns: ['StockID', 'CSUPackSize', 'co', 'branch', 'Status', 'Cat0', 'Cat1', 'Cat2', 'Cat3', 'Cat4', 'Brand', 'Selpal', 'Category0', 'Category1', 'Category2', 'Category3', 'Category4', 'Brand Name', 'StockType', 'StockCode', 'LinkCode', 'BarCode', 'SupplierCode', 'Description1', 'Description3', 'SupplierID', 'VatCode', 'PackSize', 'Units', 'Weight', 'HouseBrand', 'Variant', 'RN', 'LOOKUP', 'CASESIZE']

### stock_master
Columns: ['RecID', 'CO', 'Branch', 'StockCode', 'Variant', 'LinkCode', 'StockType', 'Units', 'Description1', 'Description2', 'DeptCode', 'SuppCode', 'BarCode', 'Supplier', 'LastCostExcl', 'LastCostIncl', 'AvgCostExcl', 'AvgCostIncl', 'BuyCostExcl', 'BuyCostIncl', 'Food', 'Category1', 'Category2', 'Category3', 'Category4', 'Status', 'QtyDecimal', 'CostDecimal', 'SellDecimal', 'SugSell', 'ListCostExcl', 'ListCostIncl', 'Binlocation', 'Weight', 'MinQty', 'MaxQty']

### purchases
Columns: ['StockID', 'CO', 'BRANCH', 'AP', 'GRVDATE', 'GRVedAccount', 'GRVedSupplier', 'DocumentType', 'STOCKCODE', 'LINKCODE', 'RECVQTY', 'RECVFREEQTY', 'RECVLINKQTY', 'RECVFREELINKQTY', 'RECVPRICE', 'RECVDISCOUNT', 'RECVTOTAL', 'RECVTAX', 'RECVNETUNIT', 'RECVNNET', 'RECVTOTALINCL', 'INTERCO']

### sales_other_info
Columns: ['SalesOtherInfo', 'TillLines', 'Feet']

### stock_onhands
Columns: ['StockCodeID', 'CO', 'BRANCH', 'STOCKCODE', 'WH', 'ONHAND', 'VAL_EXCL', 'VAL_INCL']

### suppliers
Columns: ['SupplierID', 'SupplierGroup', 'SupplierName', 'Sup_Group_Code', 'Group_Head_Buyer', 'Group_Admin_Buyer']

### sales
Columns: ['StockID', 'CustomerID', 'StockCode', 'LinkCode', 'CO', 'Branch', 'TranDate', 'TXTP', 'DocNo', 'WH', 'PriceExcl', 'AccountType', 'Quantity', 'LinkQty', 'SalesExcl', 'SalesIncl', 'CostExcl', 'CostIncl', 'GrossProfit', 'Rebate', 'NettProfit']

### stock_taxan
Columns: ['StockID', 'TxTp', 'Transaction', 'TranDate', 'WH', 'Quantity', 'LinkQty']
