use std::io;
use std::cmp::Ordering;
use rand::Rng;

fn main() {
    println!("Guess the number!");
    let secret_num = rand::thread_rng().gen_range(1..=10);
    loop {
        println!("Please input your guess.");
        let mut guess = String::new();
        io::stdin()
            .read_line(&mut guess)
            .expect("Failed to read line");
        let guess: i32 = match guess.trim().parse(){
            Ok(num) => num,
            Err(_) => continue,
        };
        println!("You guessed: {}", guess);
        match guess.cmp(&secret_num) {
            Ordering::Less => println!("Too small!"),
            Ordering::Greater => println!("Too big!"),
            Ordering::Equal => {
                println!("You win!");
                break;
            },
        };
    }
    println!("The secret number was {secret_num}, and you guessed it!");

    // let creates immutable variables, adding mut creates mutable ones
    stuff(32);
    let s = String::from("Hello");
    let m = more(&s);
    println!("{m}");
}


fn stuff(x: isize){
    println!("{x}");
}

fn more(s: &String) -> String{
    let n = String::from("Stuff");
    n
}
