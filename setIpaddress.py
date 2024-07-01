#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @file setIpaddress.py
#
#--------------------------------------------------------------------
#	setIpaddress
#		リレー　ピン番号 2～19(アナログピン 14～19) Expander (20～35)
#	python setIpaddress.py serial relay url
#--------------------------------------------------------------------
import subprocess
import sys
import datetime
import time
import serial										#pyserial
import argparse
import re
from ppadb.client import Client as AdbClient		#pure-python-adb
import json
import urllib.request,urllib.error
import base64
from datetime import datetime, timezone				#,timedelta

LOG_FILE_NAME= "ipaddress"
TEST_NAME = "setIpaddress = "
error_flag = False

usb_num_tbl = [ 7, 8, 9, 12]
pci_num_tbl = [ 5, 6, 5,  6]

client_flag = False
client = None
device = None
usb_success = False
pci_success = False
temp_success = False
cops_success = False
usb_count = 0
pci_count = 0
temp_count = 0
cops_count = 0
old_uptime= 0.0
now_uptime = 0.0
uptime_count = 0

lsmode = 0
adb_url = ""
filename = ""
start_time = ""
ser = None
uptime_list = []			#reboot 番号
process_no = 0

#-------------------------------------------------------------------
#	外部コマンド実行

def ext_connect():
	global adb_url

	cmd  = ["adb","connect","192.168.200.200"]
	cmd[2] = adb_url
	external_command(cmd)

def ext_start_server():
	cmd  = ["adb","start-server"]
	external_command(cmd)

def ext_kill_server():
	cmd  = ["adb","kill-server"]
	external_command(cmd)

#adb shell mount -o rw,remount /system
def ext_adb_shell_mount():
	cmd  = ["adb","shell","mount","-o","rw,remount","/system"]
	external_command(cmd)

#adb shell setprop persist.adb.tcp.port 5555
def ext_adb_shell_setprop():
	cmd  = ["adb","shell","setprop persist.adb.tcp.port 5555"]
	external_command(cmd)

#adb push takupato_launch.sh /system/bin/
def ext_adb_shell_push():
	cmd  = ["adb","push","takupato_launch.sh","/system/bin/"]
	external_command(cmd)

#adb pull /system/bin/takupato_launch.sh c:
def ext_adb_shell_pull():
	cmd  = ["adb","pull","/system/bin/takupato_launch.sh","C:\Freematics\python"]
	external_command(cmd)

#GPIOリセットする　echo 1 > /sys/class/edm/gpio/GPIO_P48/value
def ext_adb_gpio_reset():
	cmd  = ["adb","shell","echo 1 > /sys/class/edm/gpio/GPIO_P48/value"]
	external_command(cmd)

def external_command(cmd):

	mes = array2str(cmd)
	try:
		result = subprocess.run(cmd, encoding="utf8", shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
		set_logfile(mes)
		print(mes)
		print(result)
		return False

	except subprocess.CalledProcessError:
		mes = mes+"の実行に失敗しました"
		set_logfile(mes)
		print(mes)
		return True

	except subprocess.SubprocessError:
		mes = mes+"----> SubprocessError"
		set_logfile(mes)
		print(mes)
		return False

#	配列を文字列に変換
def array2str(array):
	count = len(array)
	mes = ""
	for n in range(count):
		mes += array[n]+" "
	#mes = "".join(array)
	return mes

#-------------------------------------------------------------------
#	ファイル操作

#	ファイル読み込み
def read_file(fname):

	flist = None
	fileobj = None
	try:
		fileobj = open(fname,'r',encoding = "utf_8_sig")
		flist = fileobj.readlines()
	except:
		print('ファイル読み込みエラー')
	finally:
		if fileobj != None:
			fileobj.close()

	return flist

#	リストファイル書きこみ
def write_file(fname,flist):
	fileobj = None
	flag = False
	try:
		fileobj = open(fname, "w", encoding = "utf_8_sig",newline="\n")
		fileobj.writelines(flist)
	except:
		print('ファイル書き込みエラー')
		flag = True
	finally:
		if fileobj != None:
			fileobj.close()
	return flag

#	ファイルのURLを書き換える
#	"ndc interface setcfg eth0 172.24.0.10 16 running multicast broadcast up"
#	"ip route add 172.24.0.0/16 dev eth0 table 4"
#
def set_file_ipaddress(flist,Ipaddress):
	check_code1 ="ndc interface setcfg eth0 "
	check_code2 = "ip route add "

	iplist = Ipaddress.split('.')
	Ipaddress2 = iplist[0]+"."+iplist[1]+'.0.0'

	for n in range(len(flist)):
		data = flist[n]
		if (re.search(check_code1,data)):
			data1 = data[len(check_code1):]
			pos = data1.find(' ')
			data2 = data1[pos:]
			data3 = check_code1+Ipaddress+data2
			#print(data3)
			flist[n] = data3

		elif (re.search(check_code2,data)):
			data1 = data[len(check_code2):]
			pos = data1.find('/')
			data2 = data1[pos:]
			data3 = check_code2+Ipaddress2+data2
			#print(data3)
			flist[n] = data3

	return flist

#キー入力待ち
def mes_yes_no(str):
	while True:
		val = input(str)
		if val == 'Y' or val== 'y':
			return True
		elif val == 'N' or val== 'n':
			return False

#-------------------------------------------------------------------

#	?? 秒 停止
def sec_wait(sec):
	time.sleep(sec)


#	ログメッセージファイル書きこみ
def set_logfile(mes):
	global filename

	fileobj = None
	try:
		if mes.count('\n') == 0:
			mes = mes+'\n'

		fileobj = open(filename, "a", encoding = "utf_8_sig")
		fileobj.write(mes)
	finally:
		if fileobj != None:
			fileobj.close()

def draw_stariTime():
	global filename
	global start_time

	start_now = datetime.now()
	start_time = start_now.strftime('%Y%m%d%H%M%S')					#elatic用
	mes = "Start time : "+start_now.strftime('%y/%m/%d %H:%M:%S')
	print(mes)
	set_logfile(mes)

#
#	コマンド送信
#
def connect_adb_sub():
	global client,device
	global adb_url

	url_port = adb_url+":5555"
	try:
		client = AdbClient(host="127.0.0.1", port=5037)
		client.remote_connect(adb_url, 5555)
		device = client.device(url_port)
		if device == None:
			mes = "unable to connect to "+url_port
		else:
			mes = "connected to "+url_port
		set_logfile(mes)
		print(mes)
		if not device == None:
			return device
		else:
			disconnect_adb()
			sec_wait(5)

	except:
		sec_wait(5)

	return None

def connect_adb():
	global client,device
	global adb_url

	for n in range(3):
		device = connect_adb_sub()
		if device != None:
			return device

	sec_wait(10)
	disconnect_adb()
	sec_wait(10)
	ext_kill_server()
	sec_wait(10)
	ext_start_server()
	sec_wait(20)
	device = connect_adb_sub()
	sec_wait(10)
	return device

def disconnect_adb():
	global adb_url
	global client

	try:
		mes= client.remote_disconnect(adb_url, 5555)
		set_logfile(mes)
		print(mes)
	except:
		mes = 'error: no such device '+str(adb_url)
		set_logfile(mes)
		print(mes)

def shell_usb_sub():
	global usb_success
	global device
	global lsmode

	try:
		sec_wait(10)
		mes = device.shell("lsusb")
		set_logfile(mes)
		count=mes.count('\n')
		if count==usb_num_tbl[lsmode-1]:
			mes2 = "SUCCESS:USB device counts is "+str(count)
			usb_success = True
		else:
			mes2 = "ERROR:USB device counts is "+str(count)

		error_flag = False

	except:
		mes = "SHELL USB ERROR ----"
		mes2=""
		error_flag = True

	set_logfile(mes2)
	print(mes+mes2)
	return error_flag

def shell_usb():
	global device
	global usb_count
	global usb_success

	usb_success = False
	uptime_err = shell_uptime(False)

	for n in range(3):
		usb_count=usb_count+1
		error_flag = shell_usb_sub()
		if error_flag == False:
			return
		else:
			sec_wait(10)
			if uptime_err == False:
				shell_uptime(True)
			disconnect_adb()
			sec_wait(10)
			device = connect_adb()
			sec_wait(10)
			if device != None:
				if uptime_err == False:
					shell_uptime(True)
				else:
					uptime_err = shell_uptime(False)

def shell_pci_sub():
	global device
	global pci_success
	global lsmode

	try:
		sec_wait(10)
		mes = device.shell("busybox lspci")
		set_logfile(mes)
		count=mes.count('\n')
		if count==pci_num_tbl[lsmode-1]:
			mes2 = "SUCCESS:PCI device counts is "+str(count)
			pci_success = True
		else:
			mes2 = "ERROR:PCI device counts is "+str(count)

		error_flag = False

	except:
		mes  = "SHELL PCI ERROR ----"
		mes2=""
		error_flag = True

	set_logfile(mes2)
	print(mes+mes2)
	return error_flag

def shell_pci():
	global pci_count
	global pci_success
	global device

	pci_success = False
	uptime_err = shell_uptime(False)

	for n in range(3):
		pci_count = pci_count+1
		error_flag = shell_pci_sub()
		if error_flag == False:
			return
		else:
			sec_wait(10)
			if uptime_err == False:
				shell_uptime(True)
			disconnect_adb()
			sec_wait(10)
			device = connect_adb()
			sec_wait(10)
			if device != None:
				if uptime_err == False:
					shell_uptime(True)
				else:
					uptime_err = shell_uptime(False)

#温度計測
def shell_temp_sub():
	global device

	try:
		sec_wait(10)
		mes = device.shell("cat /sys/class/thermal/thermal_zone0/temp")
		error_flag = False

	except:
		mes  = "SHELL TEMP ERROR ----"
		error_flag = True

	set_logfile(mes)
	print(mes)
	return error_flag

def shell_temp():
	global temp_count
	global temp_success
	global device

	temp_success = False
	uptime_err = shell_uptime(False)

	for n in range(3):
		temp_count = temp_count+1
		error_flag = shell_temp_sub()
		if error_flag == False:
			return
		else:
			sec_wait(10)
			if uptime_err == False:
				shell_uptime(True)
			disconnect_adb()
			sec_wait(10)
			device = connect_adb()
			sec_wait(10)
			if device != None:
				if uptime_err == False:
					shell_uptime(True)
				else:
					uptime_err = shell_uptime(False)

#起動時間の取得
def shell_uptime(initflag):
	global device
	global now_uptime
	global old_uptime
	global uptime_count
	global process_no
	global uptime_list

	try:
		sec_wait(5)
		mes = device.shell("cat /proc/uptime")
		uptime_mes = mes.split(' ')
		mes = 'UPTIME = '+str(uptime_mes[0])
		now_uptime = float(uptime_mes[0])
		#print('now = '+str(now_uptime)+' old = '+str(old_uptime))
		if initflag == True:
			if now_uptime < old_uptime:
				mes = mes + ' ..... May have rebooted'
				uptime_count = uptime_count+1
				if uptime_count == 1:
					uptime_list.insert(0,process_no)			#エラー番号追加
				else:
					uptime_list.append(process_no)				#エラー番号追加

		old_uptime = now_uptime
		error_flag = False

	except:
		mes  = "SHELL UPTIME ERROR ----"
		error_flag = True

	set_logfile(mes)
	print(mes)
	return error_flag

def shell_echo_sub():
	global device

	try:
		device.shell("echo 1 > /sys/class/edm/gpio/GPIO_P48/value")
		mes = "echo 1 > /sys/class/edm/gpio/GPIO_P48/value"
		error_flag = False
	except:
		mes = "SHELL GPIO48 ERROR ----"
		error_flag = True

	set_logfile(mes)
	print(mes)
	return error_flag

def shell_echo():
	global device

	for n in range(3):
		error_flag = shell_echo_sub()
		if error_flag == False:
			break
		else:
			sec_wait(10)
			disconnect_adb()
			sec_wait(10)
			device = connect_adb()
			sec_wait(10)

def shell_cops_sub():
	global device

	try:
		mes = "echo \'AT+COPS?\' > /dev/ttyUSB3"
		set_logfile(mes)
		print(mes)
		mes = device.shell("echo \'AT+COPS?\r\' > /dev/ttyUSB3")
		error_flag = False
	except:
		mes = "SHELL COPS ERROR ----"
		error_flag = True

	set_logfile(mes)
	print(mes)
	return error_flag

def shell_cops():
	global cops_count
	global cops_success
	global device

	cops_success = False
	uptime_err = shell_uptime(False)

	for n in range(3):
		cops_count = cops_count+1
		error_flag = shell_cops_sub()
		if error_flag == False:
			break
		else:
			sec_wait(10)
			if uptime_err == False:
				shell_uptime(True)
			disconnect_adb()
			sec_wait(10)
			device = connect_adb()
			sec_wait(10)
			if device != None:
				if uptime_err == False:
					shell_uptime(True)
				else:
					uptime_err = shell_uptime(False)

#
#	シリアル通信で文字をArduino側に送信
#
def relayON(serial_port,pin_no0):
	for loop in range(3):
		err_flag = send_pinNo(serial_port,pin_no0,1,1)
		if err_flag == False:
			return
	return True

def relayOFF(serial_port,pin_no0):
	for loop in range(10):
		err_flag = send_pinNo(serial_port,pin_no0,1,2)
		if err_flag == False:
			return
	return True

def send_pinNo(serial_port,pin_no0,pin_no1,on_off):
	global ser

	#relayNo = on_off*100+pin_no0*10+pin_no1
	relayNo = on_off*10000+pin_no0*100+pin_no1

	#mes = "Start setting the pin number to "+str(pin_no0) +' & '+str(pin_no1)
	mes = "Start setting the pin number to "+str(pin_no0)
	print(mes)
	set_logfile(mes)

	#print("relayNo: {}".format(relayNo))

	err_flag = False
	try:
		#ser = serial.Serial(serial_port,9600,timeout=10)
		ser = serial.Serial(serial_port,9600,dsrdtr = True)
		ser.reset_input_buffer()
		sec_wait(2)					#これがないと送信されない

#			pinNo = str(pin_no)
#			pinNo = str(relay_all = rlay_no0*10+relay_no1

#			code=bytes(str(pin_no),'utf-8')
#			code=bytes(onOff+str(pin_no)+':','utf-8')		#':'は、end codeとして使用
		code= bytes(str(relayNo)+':','utf-8')			#':'は、end codeとして使用
		#print("Send: {}".format(code))
		ser.write(code)
		sec_wait(3)					#これがないと送信されない
		# 受信
		data = ser.read(1)
		n = ser.inWaiting()
		if n: data = data + ser.read(n)
		#data = readline()
		#print("Received: {}".format(data))

		no = int(data.decode())
		if no != 999:
			on_off,pin_no2 = divmod(no,10000)
			pin_no2,pin_no3 = divmod(pin_no2,100)

#			pinNo2 = int(data.decode())-0x30
#			mes = "Set pin number to "+str(pinNo2)
#			mes = "Set pin number to "+data.decode();
			if on_off == 1:
				#mes = "Pin number "+str(pin_no2)+" & "+str(pin_no3)+" on"
				mes = "Pin number "+str(pin_no2)+" on"
			else:
				#mes = "Pin number "+str(pin_no2)+" & "+str(pin_no3)+" off"
				mes = "Pin number "+str(pin_no2)+" off"
		else:
			#mes = "Failed to set pin number "+str(pin_no0)+" & "+str(pin_no1)
			mes = "Failed to set pin number "+str(pin_no0)
			err_flag = True

		print(mes)
		set_logfile(mes)

	except:
		#mes = "Failed to set pin number "+str(pin_no0)+" & "+str(pin_no1)
		mes = "Failed to set pin number "+str(pin_no0)
		print(mes)
		set_logfile(mes)
		err_flag = True

	finally:
		if not ser == None:
			ser.close()

	return err_flag

#-------------------------------------------------------------------
#
#-------------------------------------------------------------------
def main(args):
	global filename
	global start_time
	global adb_url
	global client, device
	global uptime_count

	serial_port = args.serial
	relay_no = args.relay
	Ipaddress = args.ipaddress

	error_flag = False

	if relay_no < 2 or relay_no >35:
		print("relay error....")
		error_flag = True

	if error_flag:
		sys.exit()

	mode_success_count = 0
	usb_count = 0
	pci_count = 0
	dt_now = datetime.now()
	dt_str = dt_now.strftime('%y-%m%d-%H%M%S')
	filename = LOG_FILE_NAME+Ipaddress+'_'+str(relay_no)+'_'+dt_str+'.log'
	fmes = 'serial='+args.serial+' relay='+str(relay_no)+' ipaddress='+Ipaddress

	flist = read_file("org_takupato_launch.sh")
	flist = set_file_ipaddress(flist,Ipaddress)
	write_file("takupato_launch.sh",flist)

	print("=====================================================")
	print("    "+filename)
	#print("    "+fmes)

	set_logfile("=====================================================")
	set_logfile("    "+filename)
	#set_logfile("    "+fmes)

	adb_url = Ipaddress

	process_no = 0
	number=1
	try:
		while True:
			mm = TEST_NAME+str(process_no)+" times"
			print("=====================================================")
			print(mm)
			set_logfile("=====================================================")
			set_logfile(mm)

			draw_stariTime()
			relayON(serial_port,relay_no)
			sec_wait(30)

			if mes_yes_no("デバイスの認証は終わりましたか(y/n) ") == False:
				relayOFF(serial_port,relay_no)
				break;

			ext_adb_shell_mount()

			ext_adb_shell_setprop()

			ext_adb_shell_push()

			sec_wait(30)

			ext_adb_gpio_reset()

			sec_wait(10)
			relayOFF(serial_port,relay_no)
			print("Wait 100 seconds ....")
			sec_wait(100)

			device = connect_adb()
			sec_wait(10)
			if device != None:
				disconnect_adb()

			process_no = process_no+1
			if number != 0:
				if process_no >= number:
					break

	except KeyboardInterrupt:
		print('CTRL-C.................')

	except Exception as e:
		print("その他のエラー.........")

	#mes = '\t'+mes+' << '+str(mode_success_count)+'/'+str(n)+' >>'
	mes2 = '\t'+'reboot count'+' << '+str(uptime_count)+'/'+str(process_no)+' >>'

	set_logfile("=====================================================")
	#set_logfile(mes)
	set_logfile(mes2)
	set_logfile("=====================================================")

	print("=====================================================")
	#print(mes)
	print(mes2)
	print("=====================================================")
	print('------ '+filename+ ' ----- end')
	sys.exit()


#--------------------------------------------------------------------
#	Main Routine
#--------------------------------------------------------------------
if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='adb test')

	parser.add_argument('serial', help= 'arduino serial port')
	parser.add_argument('relay', help= 'relay no(2～35)', type=int)
	parser.add_argument('ipaddress',help= 'ipaddress(????.???.???.???')

	args = parser.parse_args()

	main(args)

