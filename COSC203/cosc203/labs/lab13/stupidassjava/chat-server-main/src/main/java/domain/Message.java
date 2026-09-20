package domain;

import java.time.LocalDateTime;

public class Message {

	private String username;
	private String message;
	private LocalDateTime time;

	public Message() {
	}

	public Message(String username, String message, LocalDateTime time) {
		this.username = username;
		this.message = message;
		this.time = time;
	}

	public String getUsername() {
		return username;
	}

	public void setUsername(String username) {
		this.username = username;
	}

	public String getMessage() {
		return message;
	}

	public void setMessage(String message) {
		this.message = message;
	}

	public LocalDateTime getTime() {
		return time;
	}

	public void setTime(LocalDateTime time) {
		this.time = time;
	}

}
