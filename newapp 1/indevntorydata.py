inventory_list = [
  {
    "InventoryID": "I001",
    "DeliveryCity": "New York",
    "NumberOfPartners": 2,
    "ProductList": [
      {
        "ProductID": "P001",
        "Quantity": 150,
        "ReorderQuantity": 100,
        "LeadTimeDays": 7,
        "WeeklySales": {
          "2024-01-01": 20,
          "2024-01-08": 25,
          "2024-01-15": 30,
          "2024-01-22": 35,
          "2024-01-29": 28,
          "2024-02-05": 32,
          "2024-02-12": 40
        }
      },
      {
        "ProductID": "P002",
        "Quantity": 75,
        "ReorderQuantity": 50,
        "LeadTimeDays": 10,
        "WeeklySales": {
          "2024-01-01": 10,
          "2024-01-08": 15,
          "2024-01-15": 12,
          "2024-01-22": 18,
          "2024-01-29": 16,
          "2024-02-05": 20,
          "2024-02-12": 22
        }
      },
      {
          "ProductID": "P003",
          "Quantity": 110,
          "ReorderQuantity": 80,
          "LeadTimeDays": 5,
          "WeeklySales": {
            "2024-01-01": 15,
            "2024-01-08": 18,
            "2024-01-15": 22,
            "2024-01-22": 20,
            "2024-01-29": 25,
            "2024-02-05": 28,
            "2024-02-12": 23
          }
      }
    ]
  },
  {
    "InventoryID": "I002",
    "DeliveryCity": "Mumbai",
    "NumberOfPartners": 3,
    "ProductList": [
      { "ProductID": "P014", "Quantity": 10, "ReorderQuantity": 15, "LeadTimeDays": 3,
        "WeeklySales": {
            "2024-01-01": 2,
            "2024-01-08": 3,
            "2024-01-15": 2,
            "2024-01-22": 4,
            "2024-01-29": 3,
            "2024-02-05": 4,
            "2024-02-12": 5
          }},
      { "ProductID": "P018", "Quantity": 7, "ReorderQuantity": 10, "LeadTimeDays": 5,
          "WeeklySales": {
            "2024-01-01": 1,
            "2024-01-08": 2,
            "2024-01-15": 3,
            "2024-01-22": 2,
            "2024-01-29": 1,
            "2024-02-05": 3,
            "2024-02-12": 2
          }},
      { "ProductID": "P005", "Quantity": 6, "ReorderQuantity": 8, "LeadTimeDays": 2,
           "WeeklySales": {
            "2024-01-01": 3,
            "2024-01-08": 4,
            "2024-01-15": 2,
            "2024-01-22": 4,
            "2024-01-29": 5,
            "2024-02-05": 2,
            "2024-02-12": 3
          }},
      { "ProductID": "P002", "Quantity": 4, "ReorderQuantity": 6, "LeadTimeDays": 4,
          "WeeklySales": {
            "2024-01-01": 2,
            "2024-01-08": 1,
            "2024-01-15": 3,
            "2024-01-22": 2,
            "2024-01-29": 1,
            "2024-02-05": 2,
            "2024-02-12": 3
        }},
      { "ProductID": "P007", "Quantity": 2, "ReorderQuantity": 4, "LeadTimeDays": 3,
          "WeeklySales": {
            "2024-01-01": 1,
            "2024-01-08": 0,
            "2024-01-15": 2,
            "2024-01-22": 1,
            "2024-01-29": 2,
            "2024-02-05": 1,
            "2024-02-12": 0
        }},
      { "ProductID": "P009", "Quantity": 3, "ReorderQuantity": 5, "LeadTimeDays": 2,
         "WeeklySales": {
            "2024-01-01": 2,
            "2024-01-08": 2,
            "2024-01-15": 1,
            "2024-01-22": 1,
            "2024-01-29": 3,
            "2024-02-05": 2,
            "2024-02-12": 1
        } },
      { "ProductID": "P012", "Quantity": 5, "ReorderQuantity": 7, "LeadTimeDays": 4,
         "WeeklySales": {
            "2024-01-01": 1,
            "2024-01-08": 3,
            "2024-01-15": 2,
            "2024-01-22": 3,
            "2024-01-29": 1,
            "2024-02-05": 2,
            "2024-02-12": 3
        }}
    ]
  },
  {
    "InventoryID": "I003",
    "DeliveryCity": "London",
    "NumberOfPartners": 4,
    "ProductList": [
      {
        "ProductID": "P021",
        "Quantity": 120,
        "ReorderQuantity": 90,
        "LeadTimeDays": 6,
        "WeeklySales": {
            "2024-01-01": 22,
            "2024-01-08": 28,
            "2024-01-15": 30,
            "2024-01-22": 25,
            "2024-01-29": 33,
             "2024-02-05": 36,
            "2024-02-12": 32
        }
      },
        {
        "ProductID": "P025",
        "Quantity": 85,
        "ReorderQuantity": 60,
        "LeadTimeDays": 8,
          "WeeklySales": {
              "2024-01-01": 18,
              "2024-01-08": 20,
              "2024-01-15": 24,
              "2024-01-22": 21,
              "2024-01-29": 26,
               "2024-02-05": 27,
              "2024-02-12": 25
          }
      },
     { "ProductID": "P008", "Quantity": 9, "ReorderQuantity": 12, "LeadTimeDays": 3,
        "WeeklySales": {
            "2024-01-01": 3,
            "2024-01-08": 4,
            "2024-01-15": 2,
            "2024-01-22": 4,
            "2024-01-29": 3,
            "2024-02-05": 5,
            "2024-02-12": 4
        } },
      { "ProductID": "P028", "Quantity": 3, "ReorderQuantity": 5, "LeadTimeDays": 6,
       "WeeklySales": {
            "2024-01-01": 1,
            "2024-01-08": 2,
            "2024-01-15": 1,
            "2024-01-22": 3,
            "2024-01-29": 2,
            "2024-02-05": 1,
            "2024-02-12": 2
        } }
    ]
  },
    {
    "InventoryID": "I004",
    "DeliveryCity": "Tokyo",
    "NumberOfPartners": 5,
     "ProductList": [
      {
        "ProductID": "P006",
        "Quantity": 95,
          "ReorderQuantity": 70,
        "LeadTimeDays": 9,
        "WeeklySales": {
             "2024-01-01": 12,
              "2024-01-08": 15,
              "2024-01-15": 18,
             "2024-01-22": 16,
              "2024-01-29": 19,
            "2024-02-05": 21,
              "2024-02-12": 20
           }
      },
       {
         "ProductID": "P029",
        "Quantity": 30,
           "ReorderQuantity": 20,
          "LeadTimeDays": 12,
          "WeeklySales": {
              "2024-01-01": 7,
               "2024-01-08": 9,
             "2024-01-15": 8,
              "2024-01-22": 11,
              "2024-01-29": 10,
               "2024-02-05": 13,
              "2024-02-12": 12
          }
      },
        { "ProductID": "P011", "Quantity": 1, "ReorderQuantity": 2, "LeadTimeDays": 10,
         "WeeklySales": {
            "2024-01-01": 0,
            "2024-01-08": 1,
            "2024-01-15": 0,
            "2024-01-22": 1,
            "2024-01-29": 0,
            "2024-02-05": 1,
            "2024-02-12": 0
         }},
        { "ProductID": "P017", "Quantity": 5, "ReorderQuantity": 8, "LeadTimeDays": 6,
          "WeeklySales": {
            "2024-01-01": 2,
            "2024-01-08": 1,
            "2024-01-15": 3,
            "2024-01-22": 2,
            "2024-01-29": 3,
            "2024-02-05": 1,
            "2024-02-12": 2
        }},
        { "ProductID": "P020", "Quantity": 2, "ReorderQuantity": 3, "LeadTimeDays": 7,
          "WeeklySales": {
            "2024-01-01": 0,
            "2024-01-08": 2,
            "2024-01-15": 1,
            "2024-01-22": 2,
            "2024-01-29": 0,
            "2024-02-05": 1,
            "2024-02-12": 0
        } }
    ]
  },
  {
    "InventoryID": "I005",
    "DeliveryCity": "Sydney",
    "NumberOfPartners": 2,
    "ProductList": [
        {
            "ProductID":"P030",
            "Quantity": 150,
              "ReorderQuantity": 110,
            "LeadTimeDays": 7,
             "WeeklySales": {
                "2024-01-01": 18,
                 "2024-01-08": 22,
                "2024-01-15": 25,
                 "2024-01-22": 20,
               "2024-01-29": 23,
                "2024-02-05": 26,
                "2024-02-12": 24
              }
          },
      {
        "ProductID": "P027",
         "Quantity": 10,
          "ReorderQuantity": 10,
          "LeadTimeDays": 8,
          "WeeklySales": {
            "2024-01-01": 5,
              "2024-01-08": 6,
            "2024-01-15": 7,
             "2024-01-22": 4,
              "2024-01-29": 7,
              "2024-02-05": 8,
             "2024-02-12": 9
        }
      },
      { "ProductID": "P004", "Quantity": 15, "ReorderQuantity": 20, "LeadTimeDays": 2,
           "WeeklySales": {
              "2024-01-01": 3,
               "2024-01-08": 4,
              "2024-01-15": 2,
               "2024-01-22": 3,
                "2024-01-29": 4,
                 "2024-02-05": 2,
                "2024-02-12": 5
        } },
      { "ProductID": "P010", "Quantity": 6, "ReorderQuantity": 8, "LeadTimeDays": 4,
          "WeeklySales": {
            "2024-01-01": 1,
            "2024-01-08": 2,
            "2024-01-15": 3,
            "2024-01-22": 2,
            "2024-01-29": 1,
            "2024-02-05": 2,
            "2024-02-12": 3
        }},
      { "ProductID": "P013", "Quantity": 3, "ReorderQuantity": 5, "LeadTimeDays": 3,
           "WeeklySales": {
            "2024-01-01": 2,
             "2024-01-08": 1,
           "2024-01-15": 2,
            "2024-01-22": 3,
            "2024-01-29": 1,
             "2024-02-05": 2,
            "2024-02-12": 1
        }},
      { "ProductID": "P015", "Quantity": 10, "ReorderQuantity": 12, "LeadTimeDays": 5,
       "WeeklySales": {
            "2024-01-01": 3,
            "2024-01-08": 2,
            "2024-01-15": 4,
            "2024-01-22": 1,
            "2024-01-29": 3,
            "2024-02-05": 2,
            "2024-02-12": 4
        } }
    ]
  }
]