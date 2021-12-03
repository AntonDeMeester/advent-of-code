# Borrowing

```rust
// This takes ownership of hello
// hello will go out of scope in the caller
fn take_onwership(hello: A) -> B {

}

// This has read only access to hello
// hello will stay in scope in the caller, and will not be changed
fn read_only(hello: &A) -> B {

}

// This has write access to hello but does not take ownership
// hello will stay in scope in the caller, and can be changed
fn read_only(hello: &mut A) -> B {

}
```
