import socket

HOST = '127.0.0.1'
PORT = 8081

#Function that sends request to the application server and returns the response
def send_request(user_request):
    try: 
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(user_request.encode())

            response = ""
            while True:
                data = s.recv(1024).decode()
                if not data:
                    break
                response += data

                if "END\n" in response or response.startswith("ERROR"):
                    break

            return response       
    except Exception as e:
        return f"ERROR {str(e)}"
    
# Function that displays results in a table
def result_output(response):
    lines = response.strip().split("\n")

    if lines[0].startswith("ERROR"):
        print(f"\n{lines[0]}\n")
        return
    
    if lines[0].startswith("OK RESULT"):
        count = int(lines[0].split()[2])
        print(f"Listings found: {count}\n")
        print("-" * 67)
        print(f"{'ID':<5} {'CITY':<15} {'ADDRESS':<25} {'PRICE':<10} {'BEDROOMS':<5}")
        print("-" * 67)

        for line in lines[1:]:
            if line == "END":
                break

            fields = {}
            for pair in line.split(";"):
                if "=" in pair:
                    key, value = pair.split("=")
                    fields[key] = value

            print(f"{fields['id']:<5} "
                  f"{fields['city']:<15} "
                  f"{fields['address']:<25} "
                  f"{fields['price']:<10} "
                  f"{fields['bedrooms']:<5} ")
        print()

#Main function, menu for the user        
def main():
    print("Welcome to the housing search service!")

    while True:
        print("What would you like to do?")
        user_option = input("1. SEARCH\n2. LIST\n3. QUIT\n")

        if user_option == '1':
            city = input("Enter city: ")
            while True:
                max_price = input("Enter max price: ")
                if max_price.isdigit():
                    user_request = f"SEARCH city={city} max_price={max_price}\n"
                    response = send_request(user_request)
                    result_output(response)
                    break
                else:
                    print("Please enter a valid price\n")

        elif user_option == '2':
            response = send_request("LIST\n")
            result_output(response)

        elif user_option == '3':
            send_request("QUIT\n")
            print("Goodbye!")
            break

        else:
            print("Please enter a valid input.\n")

if __name__ == "__main__":
    main()
