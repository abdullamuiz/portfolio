/**
 * Lead capture for the free marketing test (health-check.html).
 *
 * SETUP
 *  1. Open the "Health check leads" Sheet > Extensions > Apps Script.
 *  2. Delete ALL existing code, paste this whole file, press Save (Ctrl/Cmd + S).
 *  3. In the function dropdown next to Run, pick testLead and click Run.
 *     Approve the permissions (Advanced > Go to project > Allow).
 *     You should get a "Test" row in the Leads tab and a "Call request" email.
 *  4. Deploy > Manage deployments > pencil icon > Version: New version > Deploy.
 *     (Execute as: Me. Who has access: Anyone. The /exec link stays the same.)
 *
 * Every request is logged in the "Log" tab, and any error in the "Errors" tab,
 * so you can always see whether the website reached the script.
 */

var OWNER = 'muiz@islandeative.com';                          // where lead notifications go
var SHEET_ID = '1l2Hv8EZZUSXo2D0U9aWa7OKZN0whVwlOvP8Jk-etTIU'; // the Health check leads Sheet

var COLS = ['Timestamp', 'Name', 'Email', 'Wants call', 'WhatsApp', 'Usernames', 'Category', 'Business type',
  'Audiences', 'Markets', 'Islands', 'Platforms', 'Overall score',
  'Profiles', 'Platform mix', 'Content', 'Engagement', 'Community', 'Paid reach', 'Measurement', 'Resources',
  'Awareness', 'Consideration', 'Conversion', 'Loyalty', 'Advocacy', 'Biggest leak', 'Top fixes', 'Currency', 'Report date'];

function book() { return SpreadsheetApp.openById(SHEET_ID); }

function tab(name, header) {
  var ss = book();
  var sh = ss.getSheetByName(name) || ss.insertSheet(name);
  if (header && sh.getLastRow() === 0) { sh.appendRow(header); sh.setFrozenRows(1); }
  return sh;
}

function doGet() {
  return ContentService.createTextOutput('Lead capture is running');
}

function doPost(e) {
  var raw = (e && e.postData && e.postData.contents) || '';
  var lock = LockService.getScriptLock();
  try {
    lock.waitLock(20000);
    tab('Log', ['Timestamp', 'Bytes received']).appendRow([new Date(), raw.length]);

    var d = JSON.parse(raw || '{}');
    if (d.company_website) return json({ ok: true }); // spam trap: bots fill the hidden field

    var c = d.compass || {}, f = d.funnel || {};
    var email = String(d.email || '').trim();
    tab('Leads', COLS).appendRow([new Date(), d.name || '', email, d.wantsCall ? 'Yes' : 'No', d.whatsapp || '',
      d.usernames || '', d.cat || '', d.btype || '', d.audiences || '', d.markets || '', d.islands || '',
      d.platforms || '', num(d.score),
      num(c.profiles), num(c.mix), num(c.content), num(c.engage), num(c.community), num(c.paid), num(c.measure), num(c.team),
      num(f.aw), num(f.co), num(f.cv), num(f.lo), num(f.ad), d.leak || '', (d.topFixes || []).join('\n'),
      d.currency || '', d.date || '']);
    lock.releaseLock();

    // 1) The visitor's report
    if (/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) {
      var first = String(d.name || '').trim().split(' ')[0];
      var msg = {
        to: email,
        subject: 'Your social visibility and funnel report',
        body: visitorText(first, d),
        htmlBody: visitorHtml(first, d),
        name: 'Muiz · Islandeative',
        replyTo: OWNER
      };
      if (d.pdf_base64) {
        msg.attachments = [Utilities.newBlob(Utilities.base64Decode(d.pdf_base64), 'application/pdf',
          d.pdf_filename || 'social-visibility-report.pdf')];
      }
      MailApp.sendEmail(msg);
    }

    // 2) Your notification
    var summary = [d.btype, d.audiences, d.platforms].filter(function (x) { return x; }).join(' · ');
    MailApp.sendEmail({
      to: OWNER,
      subject: (d.wantsCall ? 'Call request: ' : 'New lead: ') + (d.usernames || email || 'marketing test') + ' (' + num(d.score) + '/100)',
      body: (d.name || '(no name)') + ' · ' + email + (d.whatsapp ? ' · WhatsApp ' + d.whatsapp : '') + '\n' + summary +
        '\nScore ' + num(d.score) + '/100. Biggest leak: ' + (d.leak || 'none') + '\n\n' + (d.topFixes || []).join('\n') +
        '\n\nLeads sheet: ' + book().getUrl(),
      htmlBody: '<p><b>' + esc(d.name || '(no name)') + '</b> · ' + esc(email) + (d.whatsapp ? ' · WhatsApp ' + esc(d.whatsapp) : '') + '</p>' +
        '<p>' + esc(summary) + '</p>' +
        '<p>Score <b>' + num(d.score) + '/100</b>. Biggest leak: <b>' + esc(d.leak || 'none') + '</b></p>' +
        '<p>' + esc((d.topFixes || []).join('\n')).replace(/\n/g, '<br>') + '</p>' +
        '<p><a href="' + book().getUrl() + '">Open the leads sheet</a></p>'
    });

    return json({ ok: true });
  } catch (err) {
    try { lock.releaseLock(); } catch (ignore) {}
    try { tab('Errors', ['Timestamp', 'Error', 'First 500 characters received']).appendRow([new Date(), String(err && err.stack || err), raw.slice(0, 500)]); } catch (ignore) {}
    return json({ ok: false, error: String(err) });
  }
}

function visitorText(first, d) {
  return 'Hi ' + (first || 'there') + ',\n\nThanks for taking the free marketing test. Your full report is attached as a PDF.\n\n' +
    'Your overall score was ' + num(d.score) + '/100' + (d.leak && d.leak !== 'None' ? ', and the biggest leak in your funnel is ' + d.leak : '') +
    '. The report shows the three things to fix first.\n\nIf you\'d like a hand putting it into action, reply to this email or message me on WhatsApp at +960 990 2996.\n\n' +
    'Muiz\nAbdulla Muiz Fuad · Islandeative\nhttps://abdullamuiz.github.io/portfolio/\n\nYou received this because you asked for your report. Reply "unsubscribe" and we won\'t email you again.';
}

function visitorHtml(first, d) {
  return '<p>Hi ' + esc(first || 'there') + ',</p>' +
    '<p>Thanks for taking the free marketing test. Your full report is attached as a PDF.</p>' +
    '<p>Your overall score was <b>' + num(d.score) + '/100</b>' + (d.leak && d.leak !== 'None' ? ', and the biggest leak in your funnel is <b>' + esc(d.leak) + '</b>' : '') +
    '. The report shows the three things to fix first.</p>' +
    '<p>If you\'d like a hand putting it into action, reply to this email or message me on WhatsApp at +960 990 2996.</p>' +
    '<p>Muiz<br>Abdulla Muiz Fuad · Islandeative<br><a href="https://abdullamuiz.github.io/portfolio/">abdullamuiz.github.io/portfolio</a></p>' +
    '<p style="color:#888;font-size:12px">You received this because you asked for your report. Reply "unsubscribe" and we won\'t email you again.</p>';
}

function num(v) { return (v === undefined || v === null || v === '') ? '' : v; }

function esc(s) {
  return String(s == null ? '' : s).replace(/[&<>"]/g, function (ch) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[ch]; });
}

function json(o) {
  return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON);
}

/** Run this from the editor to check everything works (it emails OWNER, not a visitor). */
function testLead() {
  var res = doPost({ postData: { contents: JSON.stringify({
    name: 'Test', email: OWNER, wantsCall: true, whatsapp: '+960 000 0000', usernames: '@test',
    cat: 'stay', btype: 'resort', audiences: 'tourists', markets: 'uk', islands: '', platforms: 'Instagram, Facebook',
    score: 66, compass: { profiles: 70, mix: 57 }, funnel: { aw: 66, co: 75, cv: 17, lo: 0, ad: 100 },
    leak: 'Loyalty', topFixes: ['1. Test fix'], currency: 'USD', date: 'test'
  }) } });
  Logger.log(res.getContent());
}
