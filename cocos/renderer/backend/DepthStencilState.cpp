/****************************************************************************
 Copyright (c) 2018-2019 Xiamen Yaji Software Co., Ltd.

 http://www.cocos2d-x.org

 Permission is hereby granted, free of charge, to any person obtaining a copy
 of this software and associated documentation files (the "Software"), to deal
 in the Software without restriction, including without limitation the rights
 to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 copies of the Software, and to permit persons to whom the Software is
 furnished to do so, subject to the following conditions:

 The above copyright notice and this permission notice shall be included in
 all copies or substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 THE SOFTWARE.
 ****************************************************************************/
 
#include "DepthStencilState.h"

#include "xxhash.h"

CC_BACKEND_BEGIN

bool StencilDescriptor::operator==(const StencilDescriptor &rhs) const
{
    return (stencilFailureOperation == rhs.stencilFailureOperation &&
            depthFailureOperation == rhs.depthFailureOperation &&
            depthStencilPassOperation == rhs.depthStencilPassOperation &&
            stencilCompareFunction == rhs.stencilCompareFunction &&
            readMask == rhs.readMask &&
            writeMask == rhs.writeMask);

}

DepthStencilState::DepthStencilState(const DepthStencilDescriptor& descriptor)
: _depthStencilInfo(descriptor)
{
    _isBackFrontStencilEqual = descriptor.backFaceStencil == descriptor.frontFaceStencil;
}

DepthStencilState::~DepthStencilState()
{}

bool DepthStencilDescriptor::operator==(const DepthStencilDescriptor &other) const {

  return (depthCompareFunction == other.depthCompareFunction
          && depthWriteEnabled == other.depthWriteEnabled
          && depthTestEnabled == other.depthTestEnabled
          && stencilTestEnabled == other.stencilTestEnabled
          && backFaceStencil == other.backFaceStencil
          && frontFaceStencil == other.frontFaceStencil);
}

std::size_t DepthStencilDescriptor::findHash() const {

  struct {
    CompareFunction depthCompareFunction;
    bool depthWriteEnabled;
    bool depthTestEnabled;
    bool stencilTestEnabled;
    StencilOperation stencilFailureOperation;
    StencilOperation depthFailureOperation;
    StencilOperation depthStencilPassOperation;
    CompareFunction stencilCompareFunction;
    unsigned int readMask;
    unsigned int writeMask;
    StencilOperation stencilFailureOperation2;
    StencilOperation depthFailureOperation2;
    StencilOperation depthStencilPassOperation2;
    CompareFunction stencilCompareFunction2;
    unsigned int readMask2;
    unsigned int writeMask2;
  } hashMe;
  memset(&hashMe, 0, sizeof(hashMe));
  hashMe.depthCompareFunction = depthCompareFunction;
  hashMe.depthWriteEnabled = depthWriteEnabled;
  hashMe.depthTestEnabled = depthTestEnabled;
  hashMe.stencilTestEnabled = stencilTestEnabled;
  hashMe.stencilFailureOperation = backFaceStencil.stencilFailureOperation;
  hashMe.depthFailureOperation = backFaceStencil.depthFailureOperation;
  hashMe.depthStencilPassOperation = backFaceStencil.depthStencilPassOperation;
  hashMe.stencilCompareFunction = backFaceStencil.stencilCompareFunction;
  hashMe.readMask = backFaceStencil.readMask;
  hashMe.writeMask = backFaceStencil.writeMask;
  hashMe.stencilFailureOperation2 = frontFaceStencil.stencilFailureOperation;
  hashMe.depthFailureOperation2 = frontFaceStencil.depthFailureOperation;
  hashMe.depthStencilPassOperation2 = frontFaceStencil.depthStencilPassOperation;
  hashMe.stencilCompareFunction2 = frontFaceStencil.stencilCompareFunction;
  hashMe.readMask2 = frontFaceStencil.readMask;
  hashMe.writeMask2 = frontFaceStencil.writeMask;
  unsigned int hash = XXH32((const void*)&hashMe, sizeof(hashMe), 0);
  return hash;
}

CC_BACKEND_END
