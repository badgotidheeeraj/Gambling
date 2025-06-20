import random
import asyncio

class GamePlay:
    @staticmethod
    def generate_crash_point():
        r = random.random()
        if r < 0.01:
            return round(random.uniform(20.0, 100.0), 2)
        elif r < 0.10:
            return round(random.uniform(5.0, 20.0), 2)
        elif r < 0.40:
            return round(random.uniform(2.0, 5.0), 2)
        else:
            return round(random.uniform(1.01, 2.0), 2)

    @staticmethod
    async def run_game_loop(websocket, tick_speed=0.1, player_cashout_point=1.1, bet_amount=100):
        crash_point = GamePlay.generate_crash_point()
        multiplier = 1.00
        cashout_done = False

        try:
            while multiplier < crash_point:
                current = round(multiplier, 2)
                await websocket.send_json({
                    "multiplier": current,
                    "status": "running"
                })

                # Check for auto cashout
                if not cashout_done and player_cashout_point and current >= player_cashout_point:
                    win_amount = round(bet_amount * player_cashout_point, 2)
                    await websocket.send_json({
                        "multiplier": current,
                        "status": "✅ cashed_out",
                        "win": True,
                        "amount": win_amount
                    })
                    cashout_done = True
                    break  # Stop loop on successful cashout

                await asyncio.sleep(tick_speed)
                multiplier += 0.01 * multiplier

            # If game crashed before cashout
            if not cashout_done:
                await websocket.send_json({
                    "multiplier": round(multiplier, 2),
                    "status": "💥 crashed",
                    "crash_point": crash_point,
                    "win": False,
                    "amount": 0
                })

        except Exception as e:
            print("WebSocket connection error:", e)

    @staticmethod
    def cash_out(crash_point, player_cashout_point, bet_amount):
        if player_cashout_point <= crash_point:
            return True, round(bet_amount * player_cashout_point, 2)
        else:
            return False, 0.0
