# -*- coding: utf-8 -*-
from django.http import HttpResponse
import requests
from xml.etree import ElementTree
from ccc_friend_schedule.models import Attendance
from django.core.urlresolvers import reverse
from django.conf import settings
import os

SCHEDULE_URL = 'http://events.ccc.de/congress/2014/Fahrplan/schedule.xml'
SCHEDULE_FILENAME = os.path.join(settings.BASE_DIR, 'media', 'schedule.xml')

def get_schedule_xml():
	schedule_file = open(SCHEDULE_FILENAME, 'r')
	schedule_xml = schedule_file.read()
	schedule_file.close()
	return schedule_xml

def schedule(req):
	friend_tokens = req.GET.get('friends', '')
	friend_tokens = friend_tokens.split(',')
	current_user_token = req.GET.get('me')
	attendancies = Attendance.objects.filter(user_token__in = friend_tokens)
	schedule_xml = get_schedule_xml()
	schedule_root = ElementTree.fromstring(schedule_xml)
	# Parse every event
	for event in schedule_root.findall('day/room/event'):
		event_id = event.attrib.get('id')
		event_attendancies = attendancies.filter(event_id = event_id)
		persons = event.find('persons')
		for attendance in event_attendancies:
			new_person = ElementTree.Element('person')
			new_person.text = u'♥ %s' % attendance.user_token
			persons.append(new_person)
		# Add an attendance link
		if current_user_token:
			links = event.find('links')
			new_link = ElementTree.Element('link')
			attend_href = req.build_absolute_uri(reverse('attend', kwargs={
				'user_token': current_user_token, 'event_id': event_id }))
			new_link.attrib['href'] = attend_href
			new_link.text = u'Tell others you will attend!'
			links.append(new_link)
	return HttpResponse( ElementTree.tostring(schedule_root, encoding='utf8') )

def attend(req, user_token, event_id):
	attendance, created = Attendance.objects.get_or_create(user_token=user_token, event_id=event_id)
	if attendance.id:
		return HttpResponse('ok %u' % attendance.id)
	else:
		return HttpResponse('error')