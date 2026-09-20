package dao;

import com.google.common.collect.EvictingQueue;
import domain.Message;
import java.time.LocalDateTime;
import java.util.Collection;

/**
 * A DAO that uses an EvictingQueue (Gauva) for storing the 20 most recent
 * messages.
 */
public final class MessageCollectionsDAO implements MessageDAO {

	private static final EvictingQueue messages = EvictingQueue.create(MESSAGES_TO_RETAIN);

	{
		// add a dummy message
		messages.add(new Message("Botty McBotface", "Hello", LocalDateTime.now()));
	}

	@Override
	public void addMessage(Message message) {
		messages.add(message);
	}

	@Override
	public Collection<Message> getMessages() {
		return messages;
	}

}
