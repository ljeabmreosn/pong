#!/usr/bin/env python3.6
import argparse
import matplotlib.pyplot as plt
import pygame
import re
import sys
import time

DOUBLE = r'(-?\d+\.?\d*)'
POSITION_PATTERN = re.compile(f'x: {DOUBLE}, y: {DOUBLE},.* paddle: {DOUBLE}')
SCORE_PATTERN = re.compile(r'(\d+) bounces.')

def main(args):
  size = (args.width, args.height)
  PADDLE_LENGTH = 0.4 / 2. * args.height
  done = False
  games = 0
  bounces = []

  for line in sys.stdin:
    m = re.search(SCORE_PATTERN, line)
    if m:
      print(line)
      games += 1
      if args.plot:
        bounces.append(int(m.group(1)))
      continue
    elif games < args.game_delay:
      continue
    elif games == args.game_delay:
      pygame.init()
      screen = pygame.display.set_mode(size)
      clock = pygame.time.Clock()

    if done:
      break
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        done = True

    m = re.search(POSITION_PATTERN, line)
    if m:
      x = int((args.width / 2.) * float(m.group(1)) + (args.width / 2.))
      y = int((args.height / 2.) * float(m.group(2)) + (args.height / 2.))
      paddle = int(args.height * ((1. + float(m.group(3))) / 2.))

      # print(x, y, paddle)

      screen.fill((0xff, 0xff, 0xff))
      pygame.draw.circle(screen, (0x00, 0x00, 0x00), (x, y), 10)
      rect = (
          args.width-10,
          paddle - (PADDLE_LENGTH / 2.),
          10,
          PADDLE_LENGTH,
      )
      pygame.draw.rect(screen, (0x00, 0x00, 0x00), rect)
      pygame.display.flip()
      clock.tick(args.speed)

  if args.plot:
    plt.scatter(*zip(*enumerate(bounces)), marker='.')
    plt.show()

if __name__ == '__main__':
  parser = argparse.ArgumentParser('View pong ball')
  parser.add_argument('--width', type=int, default=400)
  parser.add_argument('--height', type=int, default=400)
  parser.add_argument('--speed', type=float, default=60, help='updates per second')
  parser.add_argument('--game-delay', type=float, default=0, help='when to start showing games')
  parser.add_argument('--plot', action='store_true')
  args = parser.parse_args()
  main(args)

