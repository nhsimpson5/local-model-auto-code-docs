// Edge-case C++ fixture: exercises class members that are NOT plain
// inline definitions, to make sure class/struct source trimming copes.

#include <string>

namespace edgecases {

class Resource {
public:
    Resource() = default;
    ~Resource() = default;

    Resource(const Resource&) = delete;
    Resource& operator=(const Resource&) = delete;

    explicit Resource(std::string name) : name_(std::move(name)) {
        loaded_ = true;
    }

    void declared_elsewhere();

    virtual void must_override() = 0;

    static int instance_count() {
        return count_;
    }

    bool operator==(const Resource& other) const {
        return name_ == other.name_;
    }

private:
    std::string name_;
    bool loaded_ = false;
    static int count_;
};

void Resource::declared_elsewhere() {
    loaded_ = false;
}

struct Config {
    int width;
    int height;
};

struct Bounds {
    int min;
    int max;

    int span() const {
        return max - min;
    }
};

}  // namespace edgecases
