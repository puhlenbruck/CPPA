from app import app
ascii=''
with open('ascii.txt', 'r') as myfile:
    ascii=myfile.read()
print(ascii)
if __name__ == '__main__':
	app.run(debug = True)
