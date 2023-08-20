-- CreateEnum
CREATE TYPE "GameStatus" AS ENUM ('open', 'active', 'ended_draw', 'ended_win');

-- CreateEnum
CREATE TYPE "GameCell" AS ENUM ('A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3');

-- AlterTable
ALTER TABLE "User" ADD COLUMN     "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP;

-- CreateTable
CREATE TABLE "Move" (
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "userId" INTEGER NOT NULL,
    "gameId" INTEGER NOT NULL,
    "cell" "GameCell" NOT NULL,

    CONSTRAINT "Move_pkey" PRIMARY KEY ("userId","gameId","cell")
);

-- CreateTable
CREATE TABLE "UsersOnGames" (
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "userId" INTEGER NOT NULL,
    "gameId" INTEGER NOT NULL,

    CONSTRAINT "UsersOnGames_pkey" PRIMARY KEY ("gameId","userId")
);

-- CreateTable
CREATE TABLE "Game" (
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "id" SERIAL NOT NULL,
    "winnerId" INTEGER,
    "playerToMove" INTEGER NOT NULL,
    "status" "GameStatus" NOT NULL,

    CONSTRAINT "Game_pkey" PRIMARY KEY ("id")
);

-- AddForeignKey
ALTER TABLE "Move" ADD CONSTRAINT "Move_userId_fkey" FOREIGN KEY ("userId") REFERENCES "User"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Move" ADD CONSTRAINT "Move_gameId_fkey" FOREIGN KEY ("gameId") REFERENCES "Game"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "UsersOnGames" ADD CONSTRAINT "UsersOnGames_userId_fkey" FOREIGN KEY ("userId") REFERENCES "User"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "UsersOnGames" ADD CONSTRAINT "UsersOnGames_gameId_fkey" FOREIGN KEY ("gameId") REFERENCES "Game"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
