import { Product } from '../types';

export const products: Product[] = [
  {
    id: '1',
    name: 'Premium Wireless Headphones',
    description: 'High-quality wireless headphones with noise cancellation',
    price: 299.99,
    image: 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800',
    category: 'Electronics',
    stock: 15,
    rating: 4.5,
    reviews: [
      {
        id: 'r1',
        userId: 'u1',
        userName: 'John Doe',
        rating: 5,
        comment: 'Amazing sound quality!',
        date: '2024-03-10',
      }
    ],
  },
  {
    id: '2',
    name: 'Smart Watch Pro',
    description: 'Advanced smartwatch with health tracking features',
    price: 199.99,
    image: 'https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=800',
    category: 'Electronics',
    stock: 0,
    rating: 4.7,
    reviews: [],
    isDelayed: true,
    delayReason: 'stock',
  },
  {
    id: '3',
    name: 'Premium Coffee Maker',
    description: 'Professional grade coffee maker for home use',
    price: 159.99,
    image: 'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=800',
    category: 'Appliances',
    stock: 5,
    rating: 4.3,
    reviews: [],
    isDelayed: true,
    delayReason: 'weather',
  },
  {
    "id": "P001",
    "name": "Apple iPhone 15 Pro",
    "description": "The latest iPhone with cutting-edge features.",
    "price": 1099.00,
    "image": "https://www.backmarket.de/cdn-cgi/image/format%3Dauto%2Cquality%3D75%2Cwidth%3D1920/https://d2e6ccujb3mkqf.cloudfront.net/8dee5bc8-aabb-4c8b-8739-2b7db28ea365-1_c4b8e29a-77b5-4c7b-8e88-5ef6a295e133.jpg",
    "category": "Electronics",
    "stock": 50,
    "rating": 4.5,
    "reviews": [
      {
        "id": "r1",
        "userId": "U001",
        "userName": "Amit",
        "rating": 5,
        "comment": "Amazing phone, the camera is incredible!",
        "date": "2024-03-15"
      },
      {
        "id": "r2",
        "userId": "U002",
        "userName": "Priya",
        "rating": 4,
        "comment": "Love the features, but it's quite expensive.",
        "date": "2024-03-16"
      }
    ]
  },
  {
    "id": "P002",
    "name": "Samsung Galaxy S23 Ultra",
    "description": "Flagship Android phone with high-resolution camera.",
    "price": 999.00,
    "image": "https://www.backmarket.de/cdn-cgi/image/format%3Dauto%2Cquality%3D75%2Cwidth%3D1920/https://d2e6ccujb3mkqf.cloudfront.net/296615e6-d3ad-4889-b917-f2df6f4d3044-1_242e4fc3-25b6-43e0-854d-4e83ac356a51.jpg",
    "category": "Electronics",
    "stock": 45,
    "rating": 4.6,
    "reviews": [
      {
        "id": "r3",
        "userId": "U003",
        "userName": "Shri",
        "rating": 5,
        "comment": "Best Android phone I've ever used!",
        "date": "2024-03-12"
      },
      {
        "id": "r4",
        "userId": "U004",
        "userName": "Raja",
        "rating": 4,
        "comment": "Great phone but battery life could be better.",
        "date": "2024-03-13"
      }
    ]
  },
  {
    "id": "P003",
    "name": "Google Pixel 8 Pro",
    "description": "AI-powered smartphone with top-notch camera.",
    "price": 899.00,
     "image": "https://www.backmarket.de/cdn-cgi/image/format%3Dauto%2Cquality%3D75%2Cwidth%3D1920/https://d2e6ccujb3mkqf.cloudfront.net/616d63e8-cac5-4a81-a416-2787249dc634-1_ee39a151-893c-41a9-8457-3c1d43825b7c.jpg",
    "category": "Electronics",
    "stock": 60,
    "rating": 4.4,
    "reviews": [
      {
        "id": "r5",
        "userId": "U005",
        "userName": "Neha",
        "rating": 4,
        "comment": "The AI features are really impressive.",
        "date": "2024-03-14"
      },
      {
        "id": "r6",
        "userId": "U006",
        "userName": "Vikram",
        "rating": 5,
        "comment": "Excellent camera, especially in low light.",
        "date": "2024-03-17"
      }
    ]
  },
  {
    "id": "P004",
    "name": "OnePlus 11",
     "description": "High performance with fast charging.",
    "price": 749.00,
    "image": "https://www.backmarket.de/cdn-cgi/image/format%3Dauto%2Cquality%3D75%2Cwidth%3D640/https://d2e6ccujb3mkqf.cloudfront.net/00d821da-f5f9-4b95-8da9-7ac7de2e3c86-1_d2b63fbf-8467-4918-a2ef-fc8fe15fe5c4.jpg",
    "category": "Electronics",
    "stock": 55,
     "rating": 4.3,
    "reviews": [
       {
        "id": "r7",
        "userId": "U007",
        "userName": "Divya",
        "rating": 4,
        "comment": "Very smooth performance and fast charging.",
          "date": "2024-03-18"
      },
      {
        "id": "r8",
       "userId": "U008",
        "userName": "Rohan",
        "rating": 4,
        "comment": "Good value for money.",
        "date": "2024-03-19"
      }
    ]
  },
  {
    "id": "P005",
    "name": "Xiaomi 13 Pro",
     "description": "High-end performance with advanced display.",
    "price": 799.00,
    "image": "https://www.backmarket.de/cdn-cgi/image/format%3Dauto%2Cquality%3D75%2Cwidth%3D640/https://d2e6ccujb3mkqf.cloudfront.net/4aa31d34-eaf1-4894-a5d5-18285d1b5e70-1_acadbe7a-f23e-4dc8-9405-bf555bf56252.jpg",
    "category": "Electronics",
    "stock": 50,
    "rating": 4.2,
    "reviews": [
       {
        "id": "r9",
         "userId": "U009",
        "userName": "Anjali",
         "rating": 4,
         "comment": "Great display and impressive performance.",
        "date": "2024-03-20"
      },
       {
         "id": "r10",
        "userId": "U010",
        "userName": "Karan",
        "rating": 4,
         "comment": "Sleek design and fast processing.",
          "date": "2024-03-21"
      }
    ]
  },
  {
    "id": "P006",
    "name": "Sony WH-1000XM5",
     "description": "Premium noise-cancelling headphones with excellent sound.",
    "price": 349.00,
    "image": "https://www.sony.com/is/image/gwtprod/6145c1d32e6ac8e63a46c912dc33c5bb?fmt=png-alpha&wid=515&hei=515&trf=trim",
    "category": "Electronics",
    "stock": 70,
     "rating": 4.7,
    "reviews": [
      {
        "id": "r11",
         "userId": "U011",
        "userName": "Sakshi",
         "rating": 5,
         "comment": "Best noise cancelling headphones ever!",
        "date": "2024-03-22"
      },
      {
        "id": "r12",
        "userId": "U012",
        "userName": "Arjun",
        "rating": 4,
        "comment": "Very comfortable and great sound quality.",
        "date": "2024-03-23"
      }
    ]
  },
  {
    "id": "P007",
    "name": "Bose QuietComfort 45",
     "description": "Comfortable headphones with great noise cancellation.",
    "price": 299.00,
    "image": "https://assets.bose.com/content/dam/cloudassets/Bose_DAM/Web/consumer_electronics/global/products/headphones/qc-headphonearn/product_silo_image/AEM_qc-headphonearn_PDP_GALLERY_BLACK-7.png/jcr:content/renditions/cq5dam.web.600.600.png",
    "category": "Electronics",
    "stock": 80,
    "rating": 4.6,
    "reviews": [
       {
        "id": "r13",
        "userId": "U013",
        "userName": "Pooja",
         "rating": 5,
         "comment": "Excellent noise cancellation, perfect for travel.",
        "date": "2024-03-24"
      },
       {
        "id": "r14",
        "userId": "U014",
        "userName": "Vivek",
         "rating": 4,
        "comment": "Comfortable to wear for long durations.",
        "date": "2024-03-25"
      }
    ]
  },
  {
    "id": "P008",
    "name": "Sennheiser Momentum 4",
     "description":"High-end headphones with audiophile-grade sound quality.",
    "price": 329.00,
    "image": "https://m.media-amazon.com/images/I/71sLOtsK2UL._AC_SX679_.jpg",
    "category": "Electronics",
    "stock": 65,
     "rating": 4.5,
    "reviews": [
      {
        "id": "r15",
        "userId": "U015",
        "userName": "Naina",
         "rating": 5,
         "comment": "Amazing sound quality, true audiophile experience.",
        "date": "2024-03-26"
      },
      {
        "id": "r16",
       "userId": "U016",
        "userName": "Ankit",
         "rating": 4,
         "comment": "The build quality is superb.",
        "date": "2024-03-27"
      }
    ]
  },
  {
    "id": "P009",
    "name": "Apple AirPods Max",
     "description": "Premium headphones with high-fidelity sound and spatial audio.",
    "price": 549.00,
    "image": "https://encrypted-tbn0.gstatic.com/shopping?q=tbn:ANd9GcTyWzZvYnsOQG91J3N1EcApGJGhR2Ugt_ksv35v3-6bckBdOJExezadWbI20R2mXBsVy6quVfShx4nJv_krq0QIKGNzSonXxbPaSWsn_fiSNm5IZzUTm9vg",
    "category": "Electronics",
    "stock": 50,
    "rating": 4.4,
     "reviews": [
       {
         "id": "r17",
         "userId": "U017",
        "userName": "Riya",
         "rating": 4,
         "comment": "Love the spatial audio feature.",
        "date": "2024-03-28"
      },
      {
        "id": "r18",
        "userId": "U018",
        "userName": "Manish",
        "rating": 4,
        "comment": "Great sound but a bit pricey.",
        "date": "2024-03-29"
      }
    ]
  },
  {
    "id": "P010",
    "name": "Beats Studio Pro",
     "description": "Stylish headphones with powerful bass and clear sound.",
    "price": 349.00,
    "image": "https://www.beatsbydre.com/content/dam/beats/web/product/headphones/studiopro-wireless/pdp/product-carousel/black/alt/black-01-studiopro.jpg",
    "category": "Electronics",
    "stock": 75,
     "rating": 4.3,
    "reviews": [
       {
         "id": "r19",
         "userId": "U019",
        "userName": "Simran",
        "rating": 4,
         "comment": "Great bass and stylish design.",
        "date": "2024-03-30"
      },
       {
         "id": "r20",
        "userId": "U020",
        "userName": "Gaurav",
         "rating": 4,
        "comment": "Good battery life, very convenient to use.",
         "date": "2024-03-31"
      }
    ]
  },
    {
        "id": "P011",
        "name": "LG OLED C3 55-inch",
        "description": "Stunning OLED TV with perfect blacks and vibrant colors.",
        "price": 1499.00,
        "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSD8wAi72qGFxNwB3O_VAfaT7P4oAlSQ0anGA&s",
        "category": "Electronics",
        "stock": 30,
        "rating": 4.7,
        "reviews": [
            {
                "id": "r21",
                "userId": "U021",
                "userName": "Pankaj",
                "rating": 5,
                "comment": "The picture quality is absolutely amazing!",
                "date": "2024-04-01"
            },
             {
                "id": "r22",
                "userId": "U022",
                "userName": "Kavita",
                 "rating": 4,
                 "comment": "Great TV, worth the price.",
                 "date": "2024-04-02"
            }
        ]
    },
    {
        "id": "P012",
        "name": "Samsung QN90C 65-inch",
        "description": "Premium QLED TV with deep blacks and high brightness.",
        "price": 1699.00,
       "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTCs4Hs64f5jW9VhLxm7EPSCbVXYJb-jwl6WA&s",
        "category": "Electronics",
        "stock": 35,
        "rating": 4.6,
        "reviews": [
             {
                 "id": "r23",
                "userId": "U023",
                "userName": "Suman",
               "rating": 5,
               "comment": "The colors are so vibrant and clear.",
                "date": "2024-04-03"
            },
             {
                "id": "r24",
                "userId": "U024",
                "userName": "Alok",
               "rating": 4,
              "comment": "Excellent TV for gaming and movies.",
              "date": "2024-04-04"
            }
        ]
    },
    {
        "id": "P013",
        "name": "Sony Bravia X90L 55-inch",
        "description": "High-quality LED TV with excellent picture and sound.",
        "price": 1299.00,
         "image": "https://sony.scene7.com/is/image/sonyglobalsolutions/Mobile_X90L?$mediumstaticimagehotspot$&fmt=png-alpha",
        "category": "Electronics",
        "stock": 40,
        "rating": 4.5,
        "reviews": [
            {
                "id": "r25",
                "userId": "U025",
                "userName": "Deepika",
                "rating": 5,
                "comment": "Great TV with fantastic sound.",
                 "date": "2024-04-05"
            },
             {
               "id": "r26",
                 "userId": "U026",
                "userName": "Rahul",
                "rating": 4,
                "comment": "Happy with the overall performance.",
                 "date": "2024-04-06"
            }
        ]
    },
    {
        "id": "P014",
        "name": "TCL 6 Series 55-inch",
       "description": "Affordable QLED TV with great color and contrast.",
        "price": 799.00,
         "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSuIK-hSpGam4mPTl30cQjb5XYJiC6Rj59wWA&s",
        "category": "Electronics",
        "stock": 45,
        "rating": 4.3,
        "reviews": [
            {
                "id": "r27",
                "userId": "U027",
                "userName": "Priya",
               "rating": 4,
               "comment": "Good value for the price.",
                "date": "2024-04-07"
            },
            {
                "id": "r28",
                "userId": "U028",
                "userName": "Kunal",
               "rating": 4,
               "comment": "Excellent TV for the price point.",
               "date": "2024-04-08"
            }
        ]
    },
    {
        "id": "P015",
        "name": "Hisense U8K 65-inch",
        "description": "Mini-LED TV with high peak brightness and local dimming.",
        "price": 1099.00,
         "image": "https://hisense.de/wp-content/uploads/2023/06/U8K-65.png",
        "category": "Electronics",
        "stock": 38,
        "rating": 4.4,
        "reviews": [
           {
               "id": "r29",
               "userId": "U029",
                "userName": "Sneha",
                "rating": 5,
                "comment": "Amazing brightness and great picture quality.",
               "date": "2024-04-09"
            },
           {
                "id": "r30",
                 "userId": "U030",
                 "userName": "Manav",
                "rating": 4,
                "comment": "Very happy with the purchase.",
                "date": "2024-04-10"
            }
        ]
    },
    {
        "id": "P016",
        "name": "Canon EOS R6 Mark II",
       "description": "Professional full-frame mirrorless camera with high-speed autofocus.",
        "price": 2799.00,
       "image": "https://encrypted-tbn1.gstatic.com/shopping?q=tbn:ANd9GcSH6LIbSY6DZsk075RVGtM1TA-QIef86t3tgB1NAnL4838x_xg4yZkRF0DcWP7NPD77b4nCwEP5ZpYEi1cvk3qlDOAH6hjwCFem995VUxg",
        "category": "Electronics",
        "stock": 20,
        "rating": 4.8,
       "reviews": [
            {
                "id": "r31",
                "userId": "U031",
                "userName": "Rajesh",
                "rating": 5,
                "comment": "Excellent camera with superb autofocus.",
                "date": "2024-04-11"
            },
             {
                "id": "r32",
               "userId": "U032",
               "userName": "Priya",
               "rating": 4,
                "comment": "High-quality images, very good for professional photography.",
                "date": "2024-04-12"
            }
        ]
    },
    {
        "id": "P017",
        "name": "Sony Alpha a7 IV",
      "description": "High-performance full-frame camera with advanced features.",
        "price": 2499.00,
        "image": "https://encrypted-tbn2.gstatic.com/shopping?q=tbn:ANd9GcRBRWf5kynFfxPZA9Yx-Pf9npYJ49MnXYDwCywc9AqVPSFNQXzR7Bq2RxLKbcPAP9AFXF0Y4ryEJ5DvJOBCwgthF5IVMmsVDgDmlUsuAiUOzCtdPpyxQnH-",
        "category": "Electronics",
        "stock": 25,
       "rating": 4.7,
        "reviews": [
            {
                "id": "r33",
                "userId": "U033",
                "userName": "Vikram",
                "rating": 5,
               "comment": "Amazing dynamic range and great video quality.",
                "date": "2024-04-13"
            },
            {
               "id": "r34",
                 "userId": "U034",
                "userName": "Neha",
               "rating": 4,
              "comment": "Superb camera for both photos and videos.",
               "date": "2024-04-14"
            }
        ]
    },
    {
      "id": "P018",
        "name": "Nikon Z6 II",
       "description": "Reliable full-frame camera with dual card slots and robust build.",
        "price": 2199.00,
         "image": "https://www.nikon.co.uk/globalassets/digizuite/127854-en-z6ii_24-70_4_front.png/OptimizelyDesktopWebP",
      "category": "Electronics",
        "stock": 30,
       "rating": 4.6,
        "reviews": [
            {
               "id": "r35",
                "userId": "U035",
               "userName": "Suresh",
               "rating": 5,
               "comment": "Robust build and reliable performance.",
                "date": "2024-04-15"
            },
           {
                "id": "r36",
                "userId": "U036",
                "userName": "Anjali",
                "rating": 4,
                "comment": "Good value for a full-frame camera.",
                "date": "2024-04-16"
            }
        ]
    },
    {
        "id": "P019",
        "name": "Fujifilm X-T5",
        "description": "Stylish APS-C camera with classic design and great image quality.",
         "price": 1899.00,
       "image": "https://m.media-amazon.com/images/I/81vq1l2VF7L.__AC_SX300_SY300_QL70_ML2_.jpg",
       "category": "Electronics",
        "stock": 35,
      "rating": 4.5,
        "reviews": [
           {
                "id": "r37",
                "userId": "U037",
               "userName": "Rohan",
                "rating": 5,
                "comment": "Love the retro design and image output.",
                 "date": "2024-04-17"
            },
            {
               "id": "r38",
                 "userId": "U038",
                "userName": "Divya",
                "rating": 4,
                "comment": "Excellent camera for street photography.",
               "date": "2024-04-18"
            }
        ]
    },
    {
        "id": "P020",
        "name": "Panasonic Lumix GH6",
        "description": "Professional video-focused camera with advanced features.",
        "price": 1999.00,
        "image": "https://www.panasonic.com/content/dam/pim/de/de/DC/DC-GH6/DC-GH6/ast-1552015.jpg.pub.crop.pc.thumb.640.1200.jpg",
        "category": "Electronics",
        "stock": 20,
      "rating": 4.4,
        "reviews": [
            {
                "id": "r39",
                "userId": "U039",
               "userName": "Karan",
                "rating": 4,
               "comment": "Amazing video capabilities.",
                "date": "2024-04-19"
            },
             {
                "id": "r40",
                "userId": "U040",
                "userName": "Anjali",
               "rating": 4,
               "comment": "Best camera for video production.",
               "date": "2024-04-20"
            }
        ]
    },
  {
    "id": "P021",
    "name": "La Mer Crème de la Mer",
     "description": "Ultra-rich moisturizing cream for luxurious hydration.",
    "price": 380.00,
    "image": "https://www.cremedelamer.de/media/export/cms/products/responsive/lm_sku_332002_4x5_0.png?width=900&height=1125",
    "category": "Beauty",
    "stock": 60,
    "rating": 4.7,
       "reviews": [
            {
                "id": "r41",
               "userId": "U041",
                "userName": "Shweta",
                "rating": 5,
                "comment": "My skin has never felt so hydrated and smooth!",
                "date": "2024-04-21"
            },
           {
                "id": "r42",
                "userId": "U042",
               "userName": "Priyanka",
                 "rating": 4,
                "comment": "Luxurious feel and effective moisturization.",
                "date": "2024-04-22"
            }
        ]
  },
  {
    "id": "P022",
    "name": "Estée Lauder Advanced Night Repair",
     "description": "Powerful serum for overnight skin repair and rejuvenation.",
    "price": 115.00,
      "image": "https://encrypted-tbn1.gstatic.com/shopping?q=tbn:ANd9GcRlyHbuSeSdaTUL1-m9KUcNhY8t7Mn-wuAkDHS4ffU40b8xf0WiE_SpWiYV9bTqIuwIWYxaNqKW4gph6X8g5m1a0CJH4c55ARGzNGkTIgJQ5PCQmUXyprR3",
    "category": "Beauty",
    "stock": 70,
    "rating": 4.6,
      "reviews": [
            {
                "id": "r43",
                "userId": "U043",
                "userName": "Meera",
                 "rating": 5,
               "comment": "My skin looks so much healthier and brighter.",
                "date": "2024-04-23"
            },
           {
                "id": "r44",
                 "userId": "U044",
                "userName": "Anu",
                "rating": 4,
               "comment": "Great for reducing fine lines and wrinkles.",
                 "date": "2024-04-24"
            }
        ]
  },
  {
    "id": "P023",
    "name": "Drunk Elephant T.L.C. Framboos",
    "description": "AHA/BHA serum for gentle exfoliation and clearer skin.",
    "price": 90.00,
     "image": "https://www.belamax.de/cdn/shop/files/AlphaSerum.jpg?v=1709132277&width=700",
    "category": "Beauty",
    "stock": 75,
     "rating": 4.5,
        "reviews": [
            {
                "id": "r45",
                 "userId": "U045",
                "userName": "Isha",
                "rating": 4,
                "comment": "Effective for exfoliating and clearing acne.",
               "date": "2024-04-25"
            },
           {
                "id": "r46",
               "userId": "U046",
                "userName": "Kajal",
                "rating": 4,
               "comment": "My skin feels smoother after using this.",
                "date": "2024-04-26"
            }
        ]
  },
  {
      "id": "P024",
      "name": "The Ordinary Hyaluronic Acid 2%",
      "description": "Lightweight serum for intense hydration and plumping.",
      "price": 8.00,
      "image": "https://theordinary.com/dw/image/v2/BFKJ_PRD/on/demandware.static/-/Sites-deciem-master/default/dw67286abd/Images/products/The%20Ordinary/ord-hyaluronic-acid-2pct-B5-30ml-Clr-Acu.png?sw=800&sh=800&sm=fit",
      "category": "Beauty",
      "stock": 100,
      "rating": 4.4,
      "reviews": [
        {
          "id": "r47",
          "userId": "U047",
          "userName": "Sonia",
          "rating": 4,
          "comment": "Great affordable option for hydration.",
          "date": "2024-04-27"
        },
        {
          "id": "r48",
          "userId": "U048",
          "userName": "Varun",
          "rating": 4,
          "comment": "Effective and lightweight.",
          "date": "2024-04-28"
        }
      ]
    },
    {
      "id": "P025",
      "name": "CeraVe Moisturizing Cream",
      "description": "Rich, non-greasy cream for hydrating dry and sensitive skin.",
      "price": 18.00,
      "image": "https://www.no1-cosmetics.de/media/image/c4/45/30/3337875597449-CeraVe-14017671-Feuchtigkeitsspendende_Gesichtscreme-01-Gesichtscreme_Front_600x600.png",
      "category": "Beauty",
      "stock": 90,
      "rating": 4.6,
      "reviews": [
        {
          "id": "r49",
          "userId": "U049",
          "userName": "Tanvi",
          "rating": 5,
          "comment": "Excellent for dry and sensitive skin.",
          "date": "2024-04-29"
        },
        {
          "id": "r50",
          "userId": "U050",
          "userName": "Yash",
          "rating": 4,
          "comment": "Very moisturizing and non-irritating.",
          "date": "2024-04-30"
        }
      ]
    },
    {
      "id": "P026",
      "name": "Dior Rouge Dior Lipstick",
      "description": "Iconic lipstick with rich color and long-lasting wear.",
      "price": 42.00,
      "image": "https://cdn.flaconi.de/media/catalog/product/3/3/3348901658430.jpg?r=1T9oAh%3Fc%3Dde&w=453&fl=progressive&fit=scale&q=80&f=webp",
      "category": "Beauty",
      "stock": 50,
      "rating": 4.7,
      "reviews": [
        {
          "id": "r51",
          "userId": "U051",
          "userName": "Kriti",
          "rating": 5,
          "comment": "The classic red shade is just perfect!",
          "date": "2024-05-01"
        },
        {
          "id": "r52",
          "userId": "U052",
          "userName": "Varsha",
          "rating": 4,
          "comment": "Long-lasting and beautiful color payoff.",
          "date": "2024-05-02"
        }
      ]
    },
    {
      "id": "P027",
      "name": "MAC Matte Lipstick",
      "description": "Cult-classic matte lipstick with a vibrant and bold color.",
      "price": 22.00,
      "image": "https://img01.ztat.net/article/spp-media-p1/1704bde572c049beab09a3b55bead2fe/a1a43b693f1a489eb145de7adfc4e93c.jpg?imwidth=1800&filter=packshot",
      "category": "Beauty",
      "stock": 60,
      "rating": 4.5,
      "reviews": [
        {
          "id": "r53",
          "userId": "U053",
          "userName": "Pooja",
          "rating": 5,
          "comment": "Love the matte finish and bold color!",
          "date": "2024-05-03"
        },
        {
          "id": "r54",
          "userId": "U054",
          "userName": "Rajesh",
          "rating": 4,
          "comment": "Long-lasting and comfortable to wear.",
          "date": "2024-05-04"
        }
      ]
    },
    {
      "id": "P028",
      "name": "Fenty Beauty Pro Filt'r Foundation",
      "description": "Long-wearing, medium-to-full coverage foundation with a matte finish.",
      "price": 38.00,
      "image": "https://www.sephora.de/dw/image/v2/BBQW_PRD/on/demandware.static/-/Sites-masterCatalog_Sephora/default/dw8f4cb2b2/images/hi-res/all/SKU/614651_swatch.jpg?sw=585&sh=585&sm=fit",
      "category": "Beauty",
      "stock": 70,
      "rating": 4.3,
      "reviews": [
        {
          "id": "r55",
          "userId": "U055",
          "userName": "Neha",
          "rating": 4,
          "comment": "Great coverage and long-lasting.",
          "date": "2024-05-05"
        },
        {
          "id": "r56",
          "userId": "U056",
          "userName": "Arjun",
          "rating": 4,
          "comment": "Good shade range for all skin tones.",
          "date": "2024-05-06"
        }
      ]
    },
    {
      "id": "P029",
      "name": "Maybelline Fit Me Foundation",
      "description": "Affordable and popular matte foundation for everyday wear.",
      "price": 10.00,
      "image": "https://www.maybelline.co.in/-/media/project/loreal/brand-sites/mny/apac/in/products/face/foundation/fitme-matte-and-poreless-foundation/modules/product-info/common-003.jpg?rev=a20571aecbcd409795a84361f9560c52&cx=0.35&cy=0.45&cw=315&ch=472&hash=790A6DB2AD0F740B7C8F1DF376E96D50",
      "category": "Beauty",
      "stock": 80,
      "rating": 4.2,
      "reviews": [
        {
          "id": "r57",
          "userId": "U057",
          "userName": "Deepika",
          "rating": 4,
          "comment": "Great value for money.",
          "date": "2024-05-07"
        },
        {
          "id": "r58",
          "userId": "U058",
          "userName": "Rohan",
          "rating": 4,
          "comment": "Good for daily use.",
          "date": "2024-05-08"
        }
      ]
    },
    {
      "id": "P030",
      "name": "NARS Orgasm Blush",
      "description": "Iconic peach-pink blush with a subtle shimmer for a natural glow.",
      "price": 32.00,
      "image": "https://cdn2.parfumdreams.de/image/product/98872-209069-120-0.webp?box=528",
      "category": "Beauty",
      "stock": 65,
      "rating": 4.6,
      "reviews": [
        {
          "id": "r59",
          "userId": "U059",
          "userName": "Simran",
          "rating": 5,
          "comment": "Love the natural glow it gives!",
          "date": "2024-05-09"
        },
        {
          "id": "r60",
          "userId": "U060",
          "userName": "Gaurav",
          "rating": 4,
          "comment": "A must-have for a natural flush.",
          "date": "2024-05-10"
        }
      ]
    }
];

export const recommendedProducts = products.slice(0, 2);
export const trendingProducts = products.slice(1, 5);