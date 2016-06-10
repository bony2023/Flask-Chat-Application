// Setting session
$(document).ready(function() {
	$.getJSON('/chat', function(data) {
		$.session.set('userid', data.uid);
	});
});

// Sockets and events
var socket;
$(document).ready(function(){
	var endpoint = location.protocol + "//" + location.hostname;
	if(location.port && location.port !== "") {
		endpoint += (":" + location.port);
	}
	endpoint += "/chat";
	socket = io.connect(endpoint);
    socket.on('connect', function() {
		socket.emit('joined', {});
	});
    socket.on('status', function(data) {
		var con1 = $('<div />', {'class': 'row'});
		var con2 = $('<div />', {'class': 'col-xs-3'});
		var con3 = $('<div />', {'class': 'col-xs-6 chat-status'});
		var con4 = $('<p />', {text: data.msg, 'class': 'text-center'});
		con3.append(con4);
		con1.append(con2);
		con1.append(con3);
		$('.container .chat-content').append(con1);
		$(document).scrollTop($('.page-content-wrapper')[0].scrollHeight);
		refreshUsers();
    });
    socket.on('message', function(data) {
		addMessage(data);
	});
});

// Chat js
var entertoSend = true, size;
$("#menu-toggle").click(toggleMenu);
$("#leaveRoom").click(toggleMenu);
$('#attachment-err').hide();
$('.upload-progress-container').hide();

function toggleMenu() {
	$("#wrapper").toggleClass("toggled");
	if($('#menu-toggle').css('left') == '16px') {
		$('#menu-toggle').css('left', '316px');
	}
	else {
		$('#menu-toggle').css('left', '16px');
	}
	if($('#menu-toggle .glyphicon').css('left') == '34px') {
		$('#menu-toggle .glyphicon').css('left', '334px');
	}
	else {
		$('#menu-toggle .glyphicon').css('left', '34px');
	}
	if($('#enterToSend').is(':checked')) {
		entertoSend = true;
		$('.navbar-fixed-bottom textarea').attr('placeholder', 'Your message goes here. Shift+Enter for new line...');
		$('.navbar-fixed-bottom .input-group-btn').addClass("hidden");
	}
	else {
		entertoSend = false;
		$('.navbar-fixed-bottom textarea').attr('placeholder', 'Your message goes here...');
		$('.navbar-fixed-bottom .input-group-btn').removeClass('hidden');
	}
}

function showUploadErr() {
	$('#attachment-err').modal('show');
	size=0;
	$('#upload-media:file').filestyle('clear');
}

function okGo() {
	var message = $('.navbar-fixed-bottom textarea').val();
	$('.navbar-fixed-bottom textarea').val('');
	if(size) {
		$('.chat .upload-container').css('right', '0px');
		$('.upload-progress-container').show();
	}
	socket.emit('text', {msg: message});
}

$('#upload-media').bind('change', function() {
	$('#attachment-err').hide();
	size = (this.files[0].size/1024)/1024;
});

$('.navbar-fixed-bottom textarea').keyup(function(event) {
	if(entertoSend && event.keyCode == 13 && !event.shiftKey) {
		var ok = true;
		if(size > 10) {
			ok=false;
			showUploadErr();
		}
		if(ok) {
			okGo();
		}
	}
});

$('.navbar-fixed-bottom button').click(function() {
	$('#send').focus();
	var ok =true;
	if(size > 10) {
		ok=false;
		showUploadErr();
	}
	if(ok) {
		okGo();
	}
});

function exitRoom() {
	$.getJSON('/exit', function(data) {
		socket.emit('left', {});
		window.location.href='/';
	});
}

function addUser(name, id) {
	var con1 = $('<a />', {'class': 'list-group-item', 'href': '#'});
	var con2 = $('<span />', {'class': 'glyphicon glyphicon-record'});
	var con3 = $('<h4 />', {text: name});
	con1.append(con2);
	con1.append(con3);
	$('.active-members').append(con1);
}

function refreshUsers() {
	$.getJSON('/getUsers', function(data) {
		$('.active-members').empty();
		var users = jQuery.parseJSON(data.users);
		$('#sidebar-wrapper .badge').text(users.length);
		$.each(users, function() {
			addUser(this.name, 'u'+this.id);
		});
	});
}

function addMessage(data) {
	var filename = data.rid + '_' + data.uid;
	$.getJSON('/getAvatar/'+filename, function(avatarData) {
		var sentByMe = (data.uid == $.session.get('userid'))
		var con1 = $('<div />', {'class': 'row'});
		if(sentByMe) con1.append($('<div />', {'class': 'col-xs-2'}));
		var con2 = $('<div />', {'class': 'col-xs-10 chat-them-side'});
		var con3 = $('<div />', {'class': 'media'});
		var con4 = $('<a />', {'class': 'pull-left'});
		var con5 = $('<img />', {'class': 'media-object', 'src': avatarData.url, 'width':'80'});
		var con6 = $('<div />', {'class': 'media-body'});
		var con7 = $('<h4 />', {text: data.user, 'class': 'media-heading', 'style': 'font-weight: 500'});
		var con8 = $('<small />');
		var con9 = $('<i />', {text: ' ' + moment().format('h:mm A')});
		var con10 = $('<p />', {text: data.msg, 'class': 'text-justify'});
		if(sentByMe) {
			con2 = $('<div />', {'class': 'col-xs-10 chat-our-side'});
			con4 = $('<a />', {'class': 'pull-right'});
		}
		con8.append(con9);
		con7.append(con8);
		con6.append(con7);
		con4.append(con5);
		con3.append(con4);
		con3.append(con6);
		con3.append(con10);
		con2.append(con3);
		con1.append(con2);
        $('.container .chat-content').append(con1);
		$(document).scrollTop($('.page-content-wrapper')[0].scrollHeight);
	});
}