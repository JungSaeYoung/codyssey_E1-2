from game import QuizGame

def main():
    game = QuizGame()
    
    try:
        game.run()
    except KeyboardInterrupt:
        print("\n\n프로그램을 종료합니다.(keyboard interrupt)")
        game.save()
    except EOFError:
        print("\n입력 스트림이 종료되었습니다.(EOF error)")
        game.save()

if __name__ == "__main__":
    main()
