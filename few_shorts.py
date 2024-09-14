few_shots = [
    {"Question": "How many white Nike t-shirts are available",
     "SQLQuery": "select sum(stock_quantity) from t_shirts where color='White' and brand='Nike';",
     'SQLResult':"Result of SQL query",
      'Answer': "87"
     },
      {
     "Question": "How many black adidas tshirts are available",
     "SQLQuery": "select sum(stock_quantity) from t_shirts where color='Black' and brand='Adidas';",
     'SQLResult':"Result of SQL query",
      "Answer": "235"
     },
     {
      "Question": "How many Red Nike t-shirts are left in the stock",
     "SQLQuery": "select sum(stock_quantity) from t_shirts where color='Red' and brand='Nike';",
     'SQLResult':"Result of SQL query",
      "Answer": "136"
     },
     {
     "Question": "How many Black Adidas t-shirts are left in the stock",
     "SQLQuery": "select sum(stock_quantity) from t_shirts where color='Black' and brand='Adidas';",
     'SQLResult':"Result of SQL query",
      "Answer": "235"
     },
     {
     "Question": "How many Blue Van huesen t-shirts are left in the stock",
     "SQLQuery": "select sum(stock_quantity) from t_shirts where color='Blue' and brand='Van Huesen';",
     'SQLResult':"Result of SQL query",
      "Answer": "102"
     },
     {"Question": "what is the stock left for white Nike t-shirts",
     "SQLQuery": "select sum(stock_quantity) from t_shirts where color='White' and brand='Nike';",
     'SQLResult':"Result of SQL query",
      'Answer': "87"
     },
      {
     "Question": "what is the stock left for Black Adidas t-shirts",
     "SQLQuery": "select sum(stock_quantity) from t_shirts where color='Black' and brand='Adidas';",
     'SQLResult':"Result of SQL query",
      "Answer": "235"
     },
     {
      "Question": "what is the stock available for Red Nike t-shirts",
     "SQLQuery": "select sum(stock_quantity) from t_shirts where color='Red' and brand='Nike';",
     'SQLResult':"Result of SQL query",
      "Answer": "136"
     },
      {
      "Question": "How many total van huesen tshirts are left",
     "SQLQuery": "select brand,sum(stock_quantity) as total from t_shirts where brand='Van Huesen';",
     'SQLResult':"Result of SQL query",
      "Answer": "608"
     },
      {
      "Question": "How many total Nike tshirts are left",
     "SQLQuery": "select brand,sum(stock_quantity) as total from t_shirts where brand='Nike';",
     'SQLResult':"Result of SQL query",
      "Answer": "675"
     },
      {
     "Question": "what is the revenue generatd if all the Black nike t shirts with discount sold out",
     "SQLQuery": "select sum(t1.price*t1.stock_quantity-((t1.price*t1.stock_quantity*t2.pct_discount)/100)) as rev from t_shirts t1 join discounts t2 on t1.t_shirt_id=t2.t_shirt_id where t1.brand='Nike' and t1.color='Black';",
     'SQLResult':"Result of SQL query",
      "Answer": '799.200'   
     },
      {
     "Question": "what is the revenue generatd if all the Blue VanHuesen t shirts with discount sold out",
     "SQLQuery": "select sum(t1.price*t1.stock_quantity-((t1.price*t1.stock_quantity*t2.pct_discount)/100)) as rev from t_shirts t1 join discounts t2 on t1.t_shirt_id=t2.t_shirt_id where t1.brand='Van Huesen' and t1.color='Blue';",
     'SQLResult':"Result of SQL query",
      "Answer": '399.000'   
     },
      {
     "Question": "what is the revenue generatd if all the levi red t shirts without discount sold out",
     "SQLQuery": "select sum(price*stock_quantity) as rev from t_shirts where brand='Levi' and color='Red' and t_shirt_id not in(select t_shirt_id from discounts);",
     'SQLResult':"Result of SQL query",
      "Answer": '8886'   
     },
     {
     "Question": "what is the revenue generatd if all the white adidas t shirts without discount sold out",
     "SQLQuery": "select sum(price*stock_quantity) as rev from t_shirts where brand='Adidas' and color='White' and t_shirt_id not in(select t_shirt_id from discounts);",
     'SQLResult':"Result of SQL query",
      "Answer": '5024'   
     },
      {
     "Question": "what is the revenue generatd if all the van huesen blue t shirts without discount sold out",
     "SQLQuery": "select sum(price*stock_quantity) as rev from t_shirts where brand='Van Huesen' and color='Blue' and t_shirt_id not in(select t_shirt_id from discounts);",
     'SQLResult':"Result of SQL query",
      "Answer": '3872.0'   
     }
]
