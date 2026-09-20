package web;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.JsonDeserializer;
import com.google.gson.JsonPrimitive;
import com.google.gson.JsonSerializer;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

/**
 * Configures Gson to convert LocalDateTime objects to/from ISO-8601 date
 * strings.
 */
public class LocalDateTimeSerialiser {

	public Gson getSerialiser() {
		GsonBuilder builder = new GsonBuilder();

		builder

				// LocalDateTime to ISO-8601
				.registerTypeAdapter(LocalDateTime.class,
						(JsonSerializer<LocalDateTime>) (src, type, ctx)
							-> new JsonPrimitive(src.format(DateTimeFormatter.ISO_LOCAL_DATE_TIME)))

				// ISO-8601 to LocalDateTime
				.registerTypeAdapter(LocalDateTime.class,
						(JsonDeserializer<LocalDateTime>) (json, type, ctx)
							-> LocalDateTime.parse(json.getAsString(), DateTimeFormatter.ISO_LOCAL_DATE_TIME));

		return builder.create();
	}

}
