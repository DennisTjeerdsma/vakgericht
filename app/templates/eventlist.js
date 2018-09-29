<!DOCTYPE html>
{% extends "base.html" %}

<html>
{% block app_content %}
<body>
	<div class="row">
		<div class="col-xs-12 col-md-2">
			{% block lftcol %}
				{{super()}}
			{% endblock %}
		</div>
		<div class="col-xs-12 col-md-8">
            <a href="{{url_for('main.makeevent')}}" class="btn btn-default">Make event</a>
            <hr>
			{% for event in events %}
			<div class="col-xs-12 col-md-6">
				<div class="panel panel-default">
					<div class="panel-heading"><p><b>{{event.title}}</b></p></div>
					<div class="panel-body" style="min-height: 100px; max-height: 100px; overflow-y:scroll;">
						<p>{{event.body}}</p>
					</div>
					<div class="panel-footer">
						<p>{{moment(event.start_time).calendar</p>
						<p><a href="{{ url_for('main.event' , event_id=event.id) }}"><p>Details</a></p>
					</div>
				</div>
			</div>
			{% endfor %}
		</div>
		<div class="col-xs-12 col-md-2">
			{% block rgtcol %}
				{{super()}}
			{% endblock %}
		</div>
	</div>
</body>
{% endblock %}
</html>

{% block scripts %}
	{{super()}}
	{{ moment.include_moment() }}

{% endblock %}


