package web;

import dao.MessageDAO;
import domain.Message;
import io.jooby.Jooby;
import io.jooby.StatusCode;

public class ChatModule extends Jooby {

	public ChatModule(MessageDAO dao) {

		path("/api/messages", () -> {

			get("", ctx -> dao.getMessages());

			post("", ctx -> {
				Message message = ctx.body().to(Message.class);
				dao.addMessage(message);
				return ctx.send(StatusCode.CREATED);
			});

		});
	}

}
