% setdefault('current_lang', [l for l in languages if l[0] == request.locale][0])

<!DOCTYPE html>
<html class="no-js" lang="{{current_lang[0][:1]}}" dir="{{current_lang[3]}}">
<head>
    <meta charset="utf-8">
    <meta http-equiv="x-ua-compatible" content="ie=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="{{_('meta_description') if _('meta_description') != 'meta_description' else "LAGeSoNUM is a page helping refugees to access their number assigned by the LAGeSo online"}}" />

    <meta property="og:title" content="{{_('webpagetitle')}}">
    <meta property="og:image" content="http://lagesonum.de/anzeigetafel.jpg">
    <meta property="og:description" content="{{_('meta_description') if _('meta_description') != 'meta_description' else "LAGeSoNUM is a page helping refugees to access their number assigned by the LAGeSo online"}}">

    <meta name="twitter:card" content="{{_('meta_description') if _('meta_description') != 'meta_description' else "LAGeSoNUM is a page helping refugees to access their number assigned by the LAGeSo online"}}" />
    <meta name="twitter:site" content="@lagesonum" />
    <meta name="twitter:title" content="{{_('webpagetitle')}}" />
    <meta name="twitter:description" content="{{_('meta_description') if _('meta_description') != 'meta_description' else "LAGeSoNUM is a page helping refugees to access their number assigned by the LAGeSo online"}}" />
    <meta name="twitter:image" content="http://lagesonum.de/anzeigetafel.jpg" />

    <link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css">
    <script src="//code.jquery.com/jquery-1.11.3.min.js"></script>
    <script src="//maxcdn.bootstrapcdn.com/bootstrap/3.3.5/js/bootstrap.min.js" crossorigin="anonymous"></script>



    <style type="text/css">
        .center-block {
            margin: 0 auto;
            max-width: 760px;
        }
        .alert-big {
            text-align: center;
        }
        .alert-big strong {
            font-size: 42px;
        }

        body {
          padding-top: 50px;
        }
        .starter-template {
          padding: 40px 15px;
          /* text-align: center; */
        }
        .navbar-brand {
          padding: 10px 15px;
        }

        .navbar-lang-icon {
          display: inline-block;
          margin-right: 5px;
        }

        .para {
          padding: 1em 0;
        }
    </style>
    <title>{{_('webpagetitle')}}</title>
</head>
<body>
  <nav class="navbar navbar-inverse navbar-fixed-top">
    <div class="container">
      <div class="navbar-header">
        <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
          <span class="sr-only">Toggle navigation</span>
          <span class="icon-bar"></span>
          <span class="icon-bar"></span>
          <span class="icon-bar"></span>
        </button>
        <div class="navbar-brand">
          <img alt="LAGeSoNUM" src="/static/logo.png" height="30">
        </div>
      </div>
      <div id="navbar" class="collapse navbar-collapse">
        <ul class="nav navbar-nav">
          <li {{!'class="active"' if get("active") == "helpus" else ""}}><a href="{{i18n_path('/enter')}}">{{_('helpus_link')}}</a></li>
          <li {{!'class="active"' if get("active") == "query" else ""}}><a href="{{i18n_path('/query')}}">{{_('searchanumber_link')}}</a></li>
          <li {{!'class="active"' if get("active") == "display" else ""}}><a href="{{i18n_path('/display')}}">{{_('display_link')}}</a></li>
          <li {{!'class="active"' if get("active") == "about" else ""}}><a href="{{i18n_path('/about')}}">{{_('about_link')}}</a></li>
          <li {{!'class="active"' if get("active") == "impressum" else ""}}><a href="{{i18n_path('/impressum')}}">{{_('contact_link')}}</a></li>
        </ul>
        <ul class="nav navbar-nav navbar-right">
          <li class="dropdown">
            <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">
              <img src="/static/languages.png" alt="pick a language" width="20" height="20" class="navbar-lang-icon"> {{current_lang[1]}}<span class="caret"/>
            </a>
            <ul class="dropdown-menu">
              % for (code, label, trans_table, dir) in languages:
                <li>
                  <a href="{{i18n_path(request.path, code)}}">
                    {{label}}
                  </a>
                </li>
              % end
            </ul>
          </li>
        </ul>
      </div><!--/.nav-collapse -->
    </div>
  </nav>
