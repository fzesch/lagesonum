% include('views/header.tpl')

<div class="container">
      <div class="starter-template">

<h2>{{_('display_link')}}</h2>

% if len(numbers) > 0:
<p>{{_('numberdisplaytxt')  % ({'min_count': min_count, 'since': since})}}</p>

<div class="row col-xs-8" style="float:initial;">
%for number in numbers:
<div class="col-xs-4">{{number['num']}}</div>
%end
</div>
<p><br>{{_('alphabetorder')}}</p>

% include('views/footer.tpl')

% else:
<p>{{_('nonumbersentered') % ({'min_count': min_count, 'since': since})}}</p>

<h3>{{_('pleasenote_title')}}</h3>
<p>{{_(u'pleasenote')}}</p>

      </div>
</div>

% include('views/footer.tpl')


