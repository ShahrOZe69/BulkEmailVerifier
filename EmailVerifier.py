import dns.resolver
from Proxy_List_Scrapper import Scrapper, Proxy, ScrapperException
import concurrent.futures
import json
import requests
import random
import multiprocessing
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



def main():
	# file_name=input('Enter Filename? ')
	fillProxyPool()
	lock=multiprocessing.Manager().Lock()
	emails=open(FILE_NAME,encoding='utf-8').read().splitlines()
	print(f'{len(emails)} emails opened')
	#break into chunks of 5
	emails_arr=[emails[i:i + 5] for i in range(0, len(emails), 5)]
	total_length=len(emails_arr)
	with concurrent.futures.ThreadPoolExecutor(max_workers=NO_THREADS) as executor:
		executor.map(doWork, emails_arr,[lock]*(total_length),[total_length]*total_length) 
	# doWork(emails_arr[0],lock)
	with open(f'{FILE_NAME[:-4]} Result.csv','w',encoding='utf-8') as file:
		file.write('\n'.join(VERIFIED_EMAILS))	
	import winsound
	duration = 500  # milliseconds
	freq = 500  # Hz
	for i in range(20):
		winsound.Beep(freq, duration)

	input('DONE!!! PRESS any key to exit!')




def getProxyFromPool(lock):
	with lock:
		if len(PROXY_POOL)<=PROXY_POOL_RESET_VALUE:
			fillProxyPool()
		proxy=random.choice(list(PROXY_POOL.values()))
		PROXY_POOL.pop(proxy)
		print(f"Got Proxy from pool {proxy}")
		return proxy



def doWork(emails,lock,total_length):
	print("Started Work!!")
	verified=[]
	proxy=getProxyFromPool(lock)	
	for email in emails:
		print(f"Working on {email}")
		Succesful=False
		domain=email.split('@')[1]
		if checkMX(domain):
			print(f'{email} has MX')	
			while not Succesful:
				print(f"{DONE}/{total_length}")			
				try:
					log=checkEmail(email,proxy)
					# if proxy worked!!
					print(f'GOOD Proxy => {proxy}')
					if log:
						verified.append(email+','+log+','+domain)
						print(f'Verified email => {email}')
						Succesful=True
					else:
						proxy=getProxyFromPool(lock)	
				except Exception as e:
					print(f'BAD proxy => {proxy}')
					print(f"{DONE}/{total_length}")
					proxy=getProxyFromPool(lock)
		else:
			verified.append(email+','+"NO MX"+','+domain)			
	fillVeirfiedEmailList(verified,lock)
	print(f"{DONE}/{total_length}")

def fillVeirfiedEmailList(verified,lock):
	global VERIFIED_EMAILS
	global DONE
	with lock:
		VERIFIED_EMAILS+=verified
		DONE+=1
		
			


			
				




def checkMX(domain):
	my_resolver = dns.resolver.Resolver()
	my_resolver.nameservers = ['8.8.8.8','1.1.1.1']
	try:
		answers = my_resolver.resolve(domain, 'MX')
	except Exception as e:
		if "timed out" in str(e):
			return True	
		print(e)
		return False
	return True	



def checkEmail(email,proxy):
	URL=f'https://xxxx.xxx/{email}'
	response=requests.get(URL,proxies={"http":f"http://{proxy}","https": f"http://{proxy}"},timeout=30,verify=False)
	if response.content.decode()=='"You have reached the limit of 5 emails per hour"' or response.status_code!=200:
		return False	
	message=json.loads(response.content.decode())['response']['log']
	if "Server error. Cannot connect" in message:
		return "Server error. Cannot connect"
	if "MX record about" in message:
		return "MX record Not EXISTS"	
	return message






def fillProxyPool(cat='ALL'):
	global PROXY_POOL
	PROXY_POOL.clear()
	while len(PROXY_POOL)==0:
		print("Downloading Proxies")
		scrapper = Scrapper(category=cat, print_err_trace=True)
		data = scrapper.getProxies()
		for item in data.proxies:
			proxy='{}:{}'.format(item.ip, item.port)
			PROXY_POOL[proxy]=proxy
	print('ProxyPoolFilled')	

if __name__=='__main__':
	multiprocessing.freeze_support()
	print("EMAIL VERIFIER STARTED")
	#GlobalVARIABLE
	PROXY_POOL={}
	VERIFIED_EMAILS=[]
	FILE_NAME=input('Input Filename? ')
	NO_THREADS=int(input('Input Max Number of Threads? '))
	PROXY_POOL_RESET_VALUE=int(input('Proxy Pool Reset value? '))
	DONE=0
	main()
