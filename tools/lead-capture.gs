/**
 * Lead capture for the Social Visibility test (health-check.html).
 *
 * SETUP (about 10 minutes, in your Islandeative Google account):
 *  1. Create a Google Sheet, e.g. "Health check leads".
 *  2. In the Sheet: Extensions > Apps Script. Delete the sample code, paste this whole file, save.
 *  3. Deploy > New deployment > Select type: Web app.
 *     Execute as: Me.  Who has access: Anyone.  Click Deploy and authorise (allow Gmail + Sheets).
 *  4. Copy the Web app URL (ends in /exec) and set LEAD_ENDPOINT in health-check.html to it.
 *  After editing this script later: Deploy > Manage deployments > Edit > Version: New version.
 *
 * What it does: adds each lead to the "Leads" tab, emails the visitor their PDF from your
 * account, and emails you a short notification ("Call request" when they ask for a call).
 */
var OWNER = 'muiz@islandeative.com';
// Your leads sheet. Using its ID means the script works whether or not it was created from inside the Sheet.
var SHEET_ID = '1l2Hv8EZZUSXo2D0U9aWa7OKZN0whVwlOvP8Jk-etTIU';
function book() { return SpreadsheetApp.openById(SHEET_ID); }
var COLS = ['Timestamp', 'Name', 'Email', 'Wants call', 'WhatsApp', 'Usernames', 'Category', 'Business type',
  'Audiences', 'Markets', 'Islands', 'Platforms', 'Overall score',
  'Profiles', 'Platform mix', 'Content', 'Engagement', 'Community', 'Paid reach', 'Measurement', 'Resources',
  'Awareness', 'Consideration', 'Conversion', 'Loyalty', 'Advocacy', 'Biggest leak', 'Top fixes', 'Currency', 'Report date'];

function doGet() {
  return ContentService.createTextOutput('Lead capture is running');
}

function doPost(e) {
  try {
    var d = JSON.parse(e.postData.contents || '{}');
    if (d.company_website) return json({ ok: true }); // honeypot: bots fill hidden fields

    var ss = book();
    var sh = ss.getSheetByName('Leads') || ss.insertSheet('Leads');
    if (sh.getLastRow() === 0) { sh.appendRow(COLS); sh.setFrozenRows(1); }

    var c = d.compass || {}, f = d.funnel || {};
    sh.appendRow([new Date(), d.name || '', d.email || '', d.wantsCall ? 'Yes' : 'No', d.whatsapp || '', d.usernames || '',
      d.cat || '', d.btype || '', d.audiences || '', d.markets || '', d.islands || '', d.platforms || '', d.score,
      c.profiles, c.mix, c.content, c.engage, c.community, c.paid, c.measure, c.team,
      f.aw, f.co, f.cv, f.lo, f.ad, d.leak || '', (d.topFixes || []).join('\n'), d.currency || '', d.date || '']);

    var email = String(d.email || '').trim();
    if (/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) {
      var first = String(d.name || '').trim().split(' ')[0];
      var opts = {
        to: email,
        subject: 'Your social visibility and funnel report',
        htmlBody: visitorHtml(first, d),
        name: 'Muiz · Islandeative',
        replyTo: OWNER
      };
      if (d.pdf_base64) {
        opts.attachments = [Utilities.newBlob(Utilities.base64Decode(d.pdf_base64), 'application/pdf', d.pdf_filename || 'social-visibility-report.pdf')];
      }
      MailApp.sendEmail(opts);
    }

    MailApp.sendEmail({
      to: OWNER,
      subject: (d.wantsCall ? 'Call request: ' : 'New lead: ') + (d.usernames || d.email || 'health check') + ' (' + d.score + '/100)',
      htmlBody: '<p><b>' + esc(d.name || '(no name)') + '</b> · ' + esc(email) + (d.whatsapp ? ' · WhatsApp ' + esc(d.whatsapp) : '') + '</p>' +
        '<p>' + esc([d.btype, d.audiences, d.platforms].filter(String).join(' · ')) + '</p>' +
        '<p>Score <b>' + d.score + '/100</b>. Biggest leak: <b>' + esc(d.leak || 'none') + '</b></p>' +
        '<p>' + esc((d.topFixes || []).join('\n')).replace(/\n/g, '<br>') + '</p>' +
        '<p><a href="' + ss.getUrl() + '">Open the leads sheet</a></p>'
    });

    return json({ ok: true });
  } catch (err) {
    try {
      var ss2 = book();
      var log = ss2.getSheetByName('Errors') || ss2.insertSheet('Errors');
      log.appendRow([new Date(), String(err), e && e.postData ? String(e.postData.contents).slice(0, 500) : '']);
    } catch (ignore) {}
    return json({ ok: false });
  }
}

function visitorHtml(first, d) {
  return '<p>Hi ' + esc(first || 'there') + ',</p>' +
    '<p>Thanks for taking the social visibility test. Your full report is attached as a PDF.</p>' +
    '<p>Your overall score was <b>' + d.score + '/100</b>' + (d.leak && d.leak !== 'None' ? ', and the biggest leak in your funnel is <b>' + esc(d.leak) + '</b>' : '') +
    '. The report shows the three things to fix first.</p>' +
    '<p>If you’d like a hand putting it into action, reply to this email or message me on WhatsApp at +960 990 2996.</p>' +
    '<p>Muiz<br>Abdulla Muiz Fuad · Islandeative<br><a href="https://abdullamuiz.github.io/portfolio/">abdullamuiz.github.io/portfolio</a></p>' +
    '<p style="color:#888;font-size:12px">You received this because you asked for your report. Reply "unsubscribe" and we won’t email you again.</p>';
}

function esc(s) {
  return String(s == null ? '' : s).replace(/[&<>"]/g, function (ch) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[ch]; });
}

function json(o) {
  return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON);
}

/**
 * Run this once from the editor (select testLead, click Run). It asks for permissions if needed,
 * adds a test row to Leads and emails a test notification to you. Check View > Executions for errors.
 */
function testLead() {
  var res = doPost({ postData: { contents: JSON.stringify({
    name: 'Test', email: OWNER, wantsCall: true, whatsapp: '+960 000 0000', usernames: '@test',
    cat: 'stay', btype: 'resort', audiences: 'tourists', platforms: 'instagram,facebook', score: 66,
    compass: {}, funnel: {}, leak: 'Loyalty', topFixes: ['Test fix'], currency: 'USD', date: 'test'
  }) } });
  Logger.log(res.getContent());
}
