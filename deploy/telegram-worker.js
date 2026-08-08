/**
 * Приёмник заявок с сайта → сообщение в Telegram.
 *
 * Разворачивается как Cloudflare Worker. Токен бота и chat_id хранятся
 * в переменных окружения воркера, в код страницы они не попадают —
 * иначе любой посетитель прочитал бы все заявки через getUpdates.
 *
 * Переменные (задаются в настройках воркера, см. deploy/README.md):
 *   BOT_TOKEN  — токен бота от @BotFather
 *   CHAT_ID    — куда слать заявки
 *   ORIGIN     — адрес сайта, которому разрешено обращаться (https://kakestsmm.ru)
 */

const MESSENGER = { Telegram: "Telegram", WhatsApp: "WhatsApp", "Звонок": "Звонок" };

function cors(origin) {
  return {
    "Access-Control-Allow-Origin": origin,
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Max-Age": "86400",
  };
}

function esc(s) {
  return String(s == null ? "" : s)
    .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
    .slice(0, 300);
}

export default {
  async fetch(request, env) {
    const origin = env.ORIGIN || "*";
    const headers = { ...cors(origin), "Content-Type": "application/json" };

    if (request.method === "OPTIONS") {
      return new Response(null, { status: 204, headers: cors(origin) });
    }
    if (request.method !== "POST") {
      return new Response(JSON.stringify({ error: "method not allowed" }),
        { status: 405, headers });
    }

    let data;
    try {
      data = await request.json();
    } catch (e) {
      return new Response(JSON.stringify({ error: "bad json" }), { status: 400, headers });
    }

    // Ловушка для ботов: поле скрыто от людей, заполнить его может только скрипт.
    // Отвечаем успехом, чтобы спамер не понял, что заявка отброшена.
    if (data.website) {
      return new Response(JSON.stringify({ ok: true }), { status: 200, headers });
    }

    const digits = String(data.phone || "").replace(/\D/g, "");
    if (digits.length < 10 || digits.length > 15) {
      return new Response(JSON.stringify({ error: "bad phone" }), { status: 400, headers });
    }

    const name = esc(data.name) || "не указано";
    const phone = esc(data.phone);
    const way = MESSENGER[data.messenger] || "не указан";
    const page = esc(data.page);
    const when = new Date().toLocaleString("ru-RU", { timeZone: "Europe/Moscow" });

    const text =
      "<b>Заявка с сайта</b>\n\n" +
      "<b>Имя:</b> " + name + "\n" +
      "<b>Телефон:</b> <code>" + phone + "</code>\n" +
      "<b>Куда писать:</b> " + way + "\n\n" +
      "<i>" + when + " МСК</i>\n" +
      "<i>" + page + "</i>";

    const tg = await fetch(
      "https://api.telegram.org/bot" + env.BOT_TOKEN + "/sendMessage",
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          chat_id: env.CHAT_ID,
          text: text,
          parse_mode: "HTML",
          disable_web_page_preview: true,
        }),
      }
    );

    if (!tg.ok) {
      // Пишем в лог воркера, но наружу подробности не отдаём
      console.log("telegram error", tg.status, await tg.text());
      return new Response(JSON.stringify({ error: "send failed" }),
        { status: 502, headers });
    }

    return new Response(JSON.stringify({ ok: true }), { status: 200, headers });
  },
};
