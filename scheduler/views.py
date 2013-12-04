
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse
from scheduler.forms import DataEntryForm
from CspScheduler.ConstraintParser import create_schedule
import json

# Create your views here.


def formatReturnValues(resultList):
    print "HELLO WORLD"
    if resultList is None:
        return("No schedule possible.")
    else:
        newResultList = []
        for key in resultList:
            #print eachClass.data['school'], " ", eachClass.data['name']
            section = resultList[key]
            if section is None:
                newResultList.append(key.data['school']+" "+key.data['name']+" is not in the schedule")
            else:
                key = key
                value = resultList[key]
                stuff = {}
                stuff['school'] = key.data['school']
                stuff['name'] = key.data['name']
                stuff['title'] = key.data['title']
                stuff['credits'] = key.data['credits']
                stuff['section'] = value['name']
                stuff['meetings'] = value['meetings']
                for thing in stuff['meetings']:
                    thing['start_time'] = thing['start_time'].split("T")[1][:-1]
                    thing['end_time'] = thing['end_time'].split("T")[1][:-1]
                newResultList.append(stuff)
        return newResultList

def data_entry(request):
    if not request.user.is_authenticated():
        return HttpResponse("access denied..  Login <a href='/login'>here</a>.")
    elif request.method == 'POST':
        form = DataEntryForm(request.POST)
        if form.is_valid:
            classOptions = request.POST['Class_Options']
            minHours = request.POST['Minimum_Hours']
            maxHours = request.POST['Maximum_Hours']
            startTime = "2001-01-01T"+request.POST['Start_Time']+"Z"
            endTime = "2001-01-01T"+request.POST['End_Time']+"Z"
            requiredClasses = request.POST['Required_Classes']
            classList = classOptions.split("\r\n")
            minHours = int(minHours)
            maxHours = int(maxHours)
            #Times needs some work I think
            reqClassList = requiredClasses.split("\r\n")
            result = create_schedule(classList,{"max_hours":maxHours,"min_hours":minHours,"classes_needed":reqClassList,"start_time":startTime,"end_time":endTime})
            print("jah")
            print(result)
            print("no")
            newResult = formatReturnValues(result)
            #return HttpResponse(str(newResult))
            return render(request, "scheduler/result.html", {'data': newResult})
    else:
        form = DataEntryForm()
        return render(request, 'scheduler/app.html', {'form': form})