package domain;

public class Student {
    private Integer id;
    private String name;
    private String major;

    public Student() {}

    public Student(Integer id, String name, String major) {
        this.id = id;
        this.name = name;
        this.major = major;
    }

    public Integer getId() { return id; }
    public void setId(Integer id) { this.id = id; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public String getMajor() { return major; }
    public void setMajor(String major) { this.major = major; }
}
