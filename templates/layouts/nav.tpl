{% extends "layouts/header.tpl" %}
{% block nav %}
<!-- Navigation -->
<nav class="navbar navbar-default navbar-static-top" role="navigation" style="margin-bottom: 0">
  <div class="navbar-header">
    <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
      <span class="sr-only">Toggle navigation</span>
      <span class="icon-bar"></span>
      <span class="icon-bar"></span>
      <span class="icon-bar"></span>
    </button>
    <!-- <a class="navbar-brand" href="/">Charts</a> -->
  </div>
  <!-- /.navbar-header -->

  <ul class="nav navbar-top-links navbar-right">
    <!-- /.dropdown -->
    <li class="dropdown">
      <a class="dropdown-toggle" data-toggle="dropdown" href="#">
          <span>{{user_name}}</span>
        <i class="glyphicon glyphicon-user"></i>  <i class="glyphicon glyphicon-chevron-down"></i>
      </a>
      <ul class="dropdown-menu dropdown-user">
        <li><a href="#"><i class="glyphicon glyphicon-user"></i> User Profile</a>
        </li>
        <li><a href="#"><i class="glyphicon glyphicon-cog"></i> Settings</a>
        </li>
        <li class="divider"></li>
        <li><a href="/logout"><i class="glyphicon glyphicon-log-out"></i> Logout</a>
        </li>
      </ul>
      <!-- /.dropdown-user -->
    </li>
    <!-- /.dropdown -->
  </ul>
  <!-- /.navbar-top-links -->

  <div class="navbar-default sidebar" role="navigation">
    <li><a href="/" style="font-size:2.3em;color:#aaa;height:52px;padding:10px 20px">Charts</a></li>
    <div class="sidebar-nav">
      <ul class="metismenu" id="menu">
        {%for first in menus['menus']%}
          {% set item = first %}
          <li {%if item.name in menus['bread_crumbs'] %}class="active"{%endif%}>
            <a {%if item.child%}class="has-arrow" href="#" aria-expanded="false"{%else%}href="{{item.url}}" {% if item.name in menus['bread_crumbs']%}class="active"{%endif%}{%endif%}>{{item.name}}</a>
            {%if item.child%}
              <ul aria-expanded="false">
                {%for second in first.child%}
                {% set item = second %}
                <li {%if item.name in menus['bread_crumbs'] %}class="active"{%endif%}>
                  <a {%if item.child%}class="has-arrow" href="#" aria-expanded="false"{%else%}href="{{item.url}}" {% if item.name in menus['bread_crumbs']%}class="active"{%endif%}{%endif%}>{{item.name}}</a>
                  {%if item.child%}
                    <ul aria-expanded="false">
                      {%for item in second.child%}
                      <li>
                        <a href="{{item.url}}" {% if item.name in menus['bread_crumbs']%}class="active"{%endif%}>{{item.name}}</a>
                      </li>
                      {%endfor%}
                    </ul>
                  {%endif%}
                </li>
                {%endfor%}
              </ul>
            {%endif%}
          </li>
        {%endfor%}
      </ul>
    </div>
    <!-- /.sidebar-collapse -->
  </div>
  <!-- /.navbar-static-side -->
</nav>
{% endblock %}
{% block title %}
    {{menus.title}}
{% endblock %}
{% block bread_crumbs %}
<section class="content-header" style="padding:5px 0px 20px 0px">
  <h1>
    {{menus.title}}
  </h1>
  <ol class="breadcrumb">
    {%for item in menus.bread_crumbs%}
      <li><a href="#">{{item}}</a></li>
    {%endfor%}
  </ol>
</section>
{% endblock %}