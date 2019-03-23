"""Django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include

from . import doctorList_view
from . import login1_register1_view
from . import interlocution_view
from . import newOld_view
from . import accessDetails_view
from . import terminal_view
from . import area_view
from . import pul_view
from . import general_view
from . import userList_view
from . import classifiedQuery_view
from . import distinguish_view
from . import relationQuery_view
from . import entity_view
from . import search_view
from . import entityQuery_view
from . import baike_view
from . import consoles_view
from . import console_view
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('views/console/', console_view.console),
    path('views/consoles/', consoles_view.consoles),
    path('views/consoles/baike/', baike_view.baike),
    path('views/distinguish/', distinguish_view.distinguish),
    path('views/distinguish/getDistinguishData/', distinguish_view.getDistinguishData),
    path('views/distinguish/baike', baike_view.baike),
    path('views/entityQuery/', entityQuery_view.entityQuery),
    path('views/entityQuery/search/', search_view.search),
    path('views/entityQuery/search/entity/', entity_view.entity),
    path('views/relationQuery/', relationQuery_view.relationQuery),
    path('views/relationQuery/relation/', relationQuery_view.getRelation),
    path('views/relationQuery/node/', relationQuery_view.getNode),
    path('views/relationQuery/nodeRelation/', relationQuery_view.getNodeRelation),
    path('views/relationQuery/baike/', baike_view.baike),
    path('views/classifiedQuery/', classifiedQuery_view.classifiedQuery),
    path('views/classifiedQuery/getFenlei/', classifiedQuery_view.getFenlei),
    path('views/classifiedQuery/getEntity/', classifiedQuery_view.getEntity),
    path('views/classifiedQuery/baike/', baike_view.baike),
    path('views/interlocution/', interlocution_view.interlocution),
    # path('getAnswer/', interlocution_view.getAnswer),
    # re_path('views/(?P<p>\S*)/', views.pages),
    path('admin_views/userList/', userList_view.getAllUser),
    path('admin_views/userList/getUserInfo/', userList_view.getUserInfo),
    path('admin_views/userList/batchDel/', userList_view.batchdel),
    path('admin_views/userList/del/', userList_view.delById),
    path('admin_views/doctorList/', doctorList_view.getAllDoctor),
    path('admin_views/doctorList/getDoctorInfo/', doctorList_view.getDoctorInfo),
    path('doctor/shenhe/', doctorList_view.shenhe),
    path('doctor/updateAuditing/', doctorList_view.updateAuditing),
    path('doctor/del/', doctorList_view.delDoctor),
    path('doctor/batchDel/', doctorList_view.batchDelDoctor),
    path('admin_views/general/', general_view.general),
    path('admin_views/general/getCpuAndMemory/', general_view.getCpuAndMemory),
    path('admin_views/pul/', pul_view.pul),
    path('admin_views/pul/getPulData/', pul_view.getPulData),
    path('admin_views/area/', area_view.area),
    path('admin_views/area/getMapData/', area_view.getMapData),
    path('admin_views/terminal/', terminal_view.getTerminal),
    path('admin_views/terminal/getTerminalData/', terminal_view.getTerminalData),
    path('admin_views/accessDetails/', accessDetails_view.getAccessDetails),
    path('admin_views/accessDetails/getTableData/', accessDetails_view.getTableData),
    path('searchCondition/', views.searchCondition),
    path('admin_views/newOld/', newOld_view.newOld),
    path('admin_views/newOld/getNewOldData/', newOld_view.getNewOldData),
    path('doctor/login1/', login1_register1_view.login),
    path('doctor/getLogin/', login1_register1_view.getLogin),
    path('doctor/register1/', login1_register1_view.register),
    path('doctor/getRegister/', login1_register1_view.getRegister),
    path('doctor/perfectInfo/', login1_register1_view.perfectInfo),
    path('doctor/upload/', login1_register1_view.upload),
    path('doctor/uploadpaper/', login1_register1_view.uploadpaper),
    path('doctor/getPerfectInfo/', login1_register1_view.getPerfectInfo),
    path('ManualAnnotation/', include('ManualAnnotation.urls', namespace='ManualAnnotation')),
    path('accounts/', include('users.urls', namespace='users')),
]
# handler400 = views.bad_request
# handler403 = views.permission_denied
# handler404 = views.page_not_found
# handler500 = views.page_error
