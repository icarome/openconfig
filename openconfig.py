#!/usr/bin/python
# -*- coding: utf-8 -*
import sys
import os
import re
import time
import xml.etree.ElementTree as ET
import json
def read_config(config):
	i = 500
	interface_root = ET.Element('openremote', attrib={'xmlns': 'http://www.openremote.org','xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance', 'xsi:schemaLocation': 'http://www.openremote.org http://www.openremote.org/schemas/panel.xsd'})
	controller_root = ET.Element('openremote', attrib={'xmlns': 'http://www.openremote.org','xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance', 'xsi:schemaLocation': 'http://www.openremote.org http://www.openremote.org/schemas/panel.xsd'})
	components_root = ET.SubElement(controller_root, 'components')
	ET.SubElement(controller_root, 'sensors')
	commands_root = ET.SubElement(controller_root, 'commands')
	config_root = ET.SubElement(controller_root, 'config')
	ET.SubElement(config_root, 'property', attrib={'name': 'controller.applicationname', 'value': 'controller'})
	ET.SubElement(config_root, 'property', attrib={'name': 'multicast.address', 'value': '224.0.1.100'})
	ET.SubElement(config_root, 'property', attrib={'name': 'multicast.port', 'value': '3333'})
	ET.SubElement(config_root, 'property', attrib={'name': 'webapp.port', 'value': '8688'})
	ET.SubElement(config_root, 'property', attrib={'name': 'controller.groupname', 'value': 'floor20'})
	panels_root = ET.SubElement(interface_root, 'panels')
	screens_root = ET.SubElement(interface_root, 'screens')
	groups_root = ET.SubElement(interface_root, 'groups')
	for panel in config:
		pan_name = panel
		pan_id = i
		i+=1
		p_root = gen_panel(pan_name, pan_id)
		panels_root.append(p_root)
		for group in config[panel]:
			g_name = group
			g_id = i
			i+=1
			g_root = gen_group(g_name, g_id)
			ET.SubElement(p_root, 'include', attrib={'ref': str(g_id), 'type': 'group'})
			for screen in config[panel][group]:
				scr_name = screen
				scr_id = i
				i+=1
				sg_root = gen_screen_tg(scr_id)
				s_root = gen_screen(scr_name, scr_id, config[panel][group][screen]['background'])
				g_root.append(sg_root)
				for button in config[panel][group][screen]['buttons']:
					h = button[0]
					l = button[1]
					t = button[2]
					w = button[3]
					bid = i
				        cid = i+1000
			 		img_on = button[4]
					path = button[5]
					command = button[6]
					img_off = button[7]
					name = button[8]	
					a_button = gen_command_btn(h, l, t, w, bid, cid, img_on, path, command)
					x_button = a_button[0]
					c_button = a_button[1]
					com_button = a_button[2]
					components_root.append(c_button)
					commands_root.append(com_button)
					s_root.append(x_button)
					i+=1
				screens_root.append(s_root)
		groups_root.append(g_root)
	return [interface_root, controller_root]
	
					
					
					
					
						
def command_exists(root, cid):
	for command in root.find('commands'):
		if str(command.attrib['id']) == str(cid):
			return True
	return False

def gen_panel(name, pid):
	new_panel = ET.Element('panel', attrib={'id': str(pid), 'name': str(name)})
	return new_panel
	
def gen_group(name, gid):
	new_group = ET.Element('group', attrib={'id': str(gid), 'name': str(name)})
	return new_group
def gen_screen_tg(sid):
	new_screen = ET.Element('include', attrib={'ref': str(int(sid)), 'type': 'screen'})
	return new_screen
def gen_screen(name, sid, back_ground):
	new_screen = ET.Element('screen', attrib={'id': str(int(sid)), 'name': str(name),})
	back = ET.SubElement(new_screen, 'background', attrib={'fillScreen': 'true'})
	ET.SubElement(back, 'image', attrib={'src': str(back_ground)})
	return new_screen
def gen_ctrl_button(h, l, t, w, bid, cid, imgon, imgoff='', name=''):
	new_button = ET.Element('absolute', attrib={'height': str(int(h)), 'left': str(int(l)), 'top': str(int(t)), 'width':str(int(w))})
	button = ET.SubElement(new_button, 'button', attrib={'hasControlCommand': 'true', 'id': str(int(bid)), 'name': str(name)})
	button_d = ET.SubElement(button, 'default')
	img_button = ET.SubElement(button_d, 'image', attrib={'src': str(imgon)})
	button_c = ET.Element('button', attrib={'id':str(bid)})
	button_f = ET.SubElement(button_c, 'include', attrib={'type': 'command', 'ref': str(cid)})
	return [new_button, button_c]
def gen_command(cid, path, command):
	new_command = ET.Element('command', attrib={'id': str(cid), 'protocol': 'shellexe'})
	ET.SubElement(new_command, 'property', attrib={'name': 'commandParams', 'value': str(command)})
	ET.SubElement(new_command, 'property', attrib={'name': 'commandPath', 'value': str(path)})
	ET.SubElement(new_command, 'property', attrib={'name': 'name', 'value': str(command)})
	return new_command

def gen_command_btn(h, l, t, w, bid, cid, imgon, path, command, imgoff='', name=''):
	new_button = ET.Element('absolute', attrib={'height': str(int(h)), 'left': str(int(l)), 'top': str(int(t)), 'width':str(int(w))})
	button = ET.SubElement(new_button, 'button', attrib={'hasControlCommand': 'true', 'id': str(int(bid)), 'name': str(name)})
	button_d = ET.SubElement(button, 'default')
	img_button = ET.SubElement(button_d, 'image', attrib={'src': str(imgon)})
	button_c = ET.Element('button', attrib={'id':str(bid)})
	button_f = ET.SubElement(button_c, 'include', attrib={'type': 'command', 'ref': str(cid)})
	new_command = ET.Element('command', attrib={'id': str(cid), 'protocol': 'shellexe'})
	ET.SubElement(new_command, 'property', attrib={'name': 'commandParams', 'value': str(command)})
	ET.SubElement(new_command, 'property', attrib={'name': 'commandPath', 'value': str(path)})
	ET.SubElement(new_command, 'property', attrib={'name': 'name', 'value': str(command)})
	return [new_button, button_c, new_command]

if __name__ == '__main__':
	config = json.loads(open('config.json').read())
	p=read_config(config)
	ET.ElementTree(p[0]).write('panel.xml')
	ET.ElementTree(p[1]).write('controller.xml')
