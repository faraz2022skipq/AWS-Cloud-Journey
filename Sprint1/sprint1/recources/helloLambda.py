def lambda_handler(myTest, context):
    return "Hello {} {}!".format(myTest["First name"], myTest["Last name"]);