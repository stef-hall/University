package dao;

import domain.Message;
import java.util.Collection;

/**
 * A DAO for managing the storage of Message objects.
 *
 * Only the most recent 20 messages are retained.
 */
public interface MessageDAO {

	/**
	 * How many messages are kept.
	 */
	static final int MESSAGES_TO_RETAIN = 20;

	/**
	 * Adds a message to the DAO.
	 *
	 * @param aStudent The message to add.
	 */
	void addMessage(Message message);

	/**
	 * Retrieves the messages. Only the most recent 20 messages are returned.
	 *
	 * @return The collection of messages.
	 */
	Collection<Message> getMessages();

}
