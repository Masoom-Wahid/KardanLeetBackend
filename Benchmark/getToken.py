import requests
import json
username = input("Your Username (Contestant Username like : Winter2023__1): ")
password = input("The Password: ")



def main() -> None:
    data = {
        "username":username,
        "password":password
    }
    headers = {"Content-Type": "application/json"} 
    response = requests.post(
            "http://127.0.0.1:8000/api/auth/token/",
            data=json.dumps(data),
            headers=headers
    )
    if response.status_code < 300:
        data = response.json()
        with open("access.txt","w") as file:
            file.write(data["access"])
        print(data["access"])
    else:
        print(f"Invalid Username or Password with the status of {response.status_code}")



if __name__ == "__main__":
    main()